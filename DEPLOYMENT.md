# AHAB IMPEX LLP - Deployment Guide

## Pre-Deployment Checklist

### 1. Code Preparation

- [x] Logo updated to AHAB IMPEX branding
- [x] Color scheme matches brand identity (browns, golds, greens)
- [x] All branding text updated to "AHAB IMPEX LLP"
- [x] Contact information configured
- [x] WhatsApp integration set up
- [ ] Product images added to database
- [ ] Content reviewed and finalized

### 2. Django Settings for Production

Update `spice_site/settings.py`:

```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your domain
ALLOWED_HOSTS = ['ahabimpex.com', 'www.ahabimpex.com', 'your-domain.com']

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Database - Use PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'your_db_host',
        'PORT': '5432',
    }
}
```

### 3. Environment Variables

Create a `.env` file (DO NOT commit to git):

```env
SECRET_KEY=your-very-secret-key-here-change-this
DEBUG=False
DATABASE_URL=postgresql://user:password@host:5432/dbname
ALLOWED_HOSTS=ahabimpex.com,www.ahabimpex.com
```

Install python-decouple:
```bash
pip install python-decouple
```

Update settings.py to use environment variables:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

## Deployment Options

### Option 1: PythonAnywhere (Easiest for Beginners)

**Pros**: Free tier available, easy setup, good for small sites
**Cost**: Free (with limitations) or $5/month

**Steps**:

1. **Create account** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload your code**
   ```bash
   # Via Git
   git clone https://github.com/yourusername/spice_website.git
   ```

3. **Create virtual environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 spice_env
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to Web tab
   - Add new web app
   - Choose Manual configuration
   - Python 3.10
   - Set source code directory
   - Set virtualenv path

5. **Configure WSGI file**
   Edit the WSGI configuration file to point to your Django project

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Reload web app**

### Option 2: Heroku (Recommended)

**Pros**: Easy deployment, free tier, automatic SSL, good scaling
**Cost**: Free tier available, paid plans from $7/month

**Steps**:

1. **Install Heroku CLI**
   Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create ahab-impex-spices
   ```

4. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Create required files**

   **Procfile** (create in project root):
   ```
   web: gunicorn spice_site.wsgi --log-file -
   ```

   **runtime.txt**:
   ```
   python-3.11.0
   ```

   **requirements.txt** (add these):
   ```
   gunicorn==21.2.0
   psycopg2-binary==2.9.9
   dj-database-url==2.1.0
   whitenoise==6.6.0
   ```

6. **Update settings.py for Heroku**
   ```python
   import dj_database_url
   
   # Database
   DATABASES = {
       'default': dj_database_url.config(
           default='sqlite:///db.sqlite3',
           conn_max_age=600
       )
   }
   
   # Static files with WhiteNoise
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
       # ... other middleware
   ]
   
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

7. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DEBUG=False
   ```

8. **Deploy**
   ```bash
   git add .
   git commit -m "Prepare for Heroku deployment"
   git push heroku main
   ```

9. **Run migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

10. **Open your app**
    ```bash
    heroku open
    ```

### Option 3: DigitalOcean App Platform

**Pros**: Good performance, easy scaling, competitive pricing
**Cost**: From $5/month

**Steps**:

1. **Create DigitalOcean account**

2. **Create new app**
   - Connect your GitHub repository
   - Choose Python as environment

3. **Configure build settings**
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Run Command: `gunicorn spice_site.wsgi`

4. **Add database**
   - Add PostgreSQL database component
   - Note the connection string

5. **Set environment variables**
   - SECRET_KEY
   - DATABASE_URL
   - DEBUG=False

6. **Deploy**
   - Click "Deploy"
   - Wait for build to complete

### Option 4: AWS (Advanced)

**Pros**: Maximum control, excellent scalability, enterprise-grade
**Cost**: Variable, can be optimized

**Services needed**:
- EC2 (server)
- RDS (PostgreSQL database)
- S3 (static files)
- CloudFront (CDN)
- Route 53 (DNS)

**This option requires advanced knowledge of AWS services.**

## Post-Deployment Tasks

### 1. Domain Configuration

**If using custom domain**:

1. Purchase domain from registrar (Namecheap, GoDaddy, etc.)
2. Point DNS to your hosting provider:
   - Heroku: Add CNAME record
   - PythonAnywhere: Update A record
   - DigitalOcean: Update nameservers

3. Configure SSL certificate (usually automatic with modern hosts)

### 2. Set up Email

For contact forms to work:

**Option A: Gmail SMTP** (Simple)
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

**Option B: SendGrid** (Recommended for production)
```bash
pip install sendgrid
```

### 3. Set up Monitoring

**Sentry** (Error tracking):
```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
)
```

### 4. Performance Optimization

1. **Enable caching**
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

2. **Compress static files**
   - Already configured with WhiteNoise

3. **Use CDN for images**
   - Consider Cloudinary or AWS S3

### 5. Backup Strategy

1. **Database backups**
   - Heroku: Automatic with paid plans
   - Manual: `pg_dump` scheduled via cron

2. **Code backups**
   - Use Git (GitHub, GitLab, Bitbucket)

3. **Media files backups**
   - Use S3 or similar cloud storage

## Testing Before Going Live

### 1. Functionality Tests

- [ ] All pages load correctly
- [ ] Forms submit successfully
- [ ] Contact form sends emails
- [ ] WhatsApp link works
- [ ] Navigation works on mobile
- [ ] Images load properly
- [ ] Admin panel accessible

### 2. Performance Tests

- [ ] Page load time < 3 seconds
- [ ] Mobile performance score > 80 (Google PageSpeed)
- [ ] Images optimized
- [ ] CSS/JS minified

### 3. SEO Tests

- [ ] Meta tags present on all pages
- [ ] Sitemap.xml generated
- [ ] robots.txt configured
- [ ] Google Search Console set up
- [ ] Google Analytics added

### 4. Security Tests

- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] SQL injection protection (Django ORM)
- [ ] CSRF protection enabled
- [ ] XSS protection enabled

## Maintenance

### Regular Tasks

**Weekly**:
- Check error logs
- Review contact form submissions
- Update product information

**Monthly**:
- Update dependencies: `pip list --outdated`
- Review analytics
- Backup database

**Quarterly**:
- Security audit
- Performance optimization
- Content updates

## Support & Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Heroku Django Guide**: https://devcenter.heroku.com/articles/django-app-configuration
- **Django Deployment Checklist**: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

## Quick Commands Reference

```bash
# Local development
python manage.py runserver

# Create migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Heroku deployment
git push heroku main
heroku run python manage.py migrate
heroku logs --tail

# Check deployment readiness
python manage.py check --deploy
```

---

**Need help?** Contact your development team or refer to the official Django deployment documentation.

**Good luck with your deployment! 🚀**
