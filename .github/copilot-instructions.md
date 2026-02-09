## Quick orientation for AI code assistants

This is a small Django site (Django 5.2.8) for a spice company. The goal of these notes is to help an AI agent be immediately productive by highlighting project structure, conventions, and concrete examples.

### Big picture
- Django project root: `manage.py` and settings at `spice_site/settings.py`.
- Single app `pages/` implements most behavior: models, views, forms, admin and URL routes live there.
- Templates under `templates/` (global) and `templates/pages/`. Static assets are in `static/` and loaded via `STATICFILES_DIRS`.
- Database: SQLite file at project root `db.sqlite3`. Fixtures for quick data seeds in `fixtures/` (e.g. `products.json`, `faqs.json`).

Why this matters: changes to models often require migrations (see commands below). Templates rely on Django messages/context; modifying a view may require editing multiple templates.

### Key files to reference
- `spice_site/settings.py` — settings, static/media paths, and `BRANDING_CONFIG` loaded from `config.json`.
- `pages/models.py` — Product, FAQ, VisitorRegistration, ContactMessage. Note: Product.slug is auto-generated in `save()` when blank.
- `pages/views.py` — Home, product listing (`products`), `product_detail`, `register`, contact handling. `products` reads GET `category` to filter.
- `pages/admin.py` — Admin configuration (prepopulated slug, list filters, readonly fields).
- `templates/base.html` — global layout, uses Bootstrap CDN, AOS, and shows `messages` (message framework used across views).

### Developer workflows / commands (exact)
- Create venv & activate (Windows PowerShell):
  python -m venv .venv; .venv\Scripts\Activate
- Install deps (project uses Django pinned in README):
  pip install django==5.2.8
- Run migrations:
  python manage.py makemigrations pages
  python manage.py migrate
- Load fixtures (seed data):
  python manage.py loaddata fixtures/products.json
  python manage.py loaddata fixtures/faqs.json
- Create admin and run dev server:
  python manage.py createsuperuser
  python manage.py runserver

Admin UI: http://127.0.0.1:8000/admin/ (use admin to add Products/FAQs/registrations/contact messages)

### Project-specific conventions and patterns
- Slug generation: Products auto-generate `slug` using `slugify(name)` in `Product.save()` with uniqueness loop — prefer using model save or `get_or_create` carefulness when creating products programmatically.
- Category list: `Product.CATEGORY_CHOICES` is the source of truth; views build category lists via `[c for c, _ in Product.CATEGORY_CHOICES]` — modify choices here to change available categories site-wide.
- Images: `Product.image_url` expects an external URL (not uploaded files). Admin and templates assume direct image URLs (e.g., Unsplash). If you add file uploads, update models/templates/settings accordingly.
- Forms: `VisitorRegistrationForm` is a `ModelForm` used in a homepage modal; `ContactForm` is a plain `forms.Form`. Views use Django `messages` to surface form errors/success. Keep existing Bootstrap classes on widgets.
- Templates: base layout loads Bootstrap via CDN and static files using `{% static %}`. Versioning querystrings like `?v=2` is used for cache-busting — preserve when updating assets.
- Branding/config: `spice_site/settings.py` loads `config.json` into `BRANDING_CONFIG`. Use that for company name/colors rather than hard-coding.

### Integration points & cross-component notes
- Views use `Product.get_absolute_url()` and `reverse('product_detail', kwargs={'slug': slug})` — do not change `name='product_detail'` in `pages/urls.py` without updating references.
- `pages.views.register` expects POST from the homepage modal; it redirects to `home` and surfaces errors with messages — tests or changes to the modal should respect this flow.
- `templates/base.html` includes `messages` rendering; other templates rely on that behavior for user feedback.

### Examples (copy/paste-ready)
- Query products in the same style as the site:

  from pages.models import Product
  qs = Product.objects.filter(is_active=True)
  qs = qs.filter(category='Cardamom')

- Create a product while letting slug logic run:

  p = Product.objects.create(name='Green Cardamom', category='Cardamom', price=12.50, image_url='https://...')

### Safety / deployment notes
- Settings currently have DEBUG=True and the SECRET_KEY checked into `settings.py` — do not assume production readiness. For deployments set DEBUG=False, rotate the SECRET_KEY, and configure static/media hosting and a WSGI/ASGI server.
- `STATIC_ROOT` is set to `staticfiles` in settings; collect static files before production use.

### Missing / not present
- There are no automated tests in the repo. If you add tests, follow Django standard `tests.py` placement under `pages/` or a `tests/` package.

If any part of this guidance is unclear or you want the doc to include more examples (e.g., ORM snippets, recommended PR checklist, or a small test harness), tell me which sections to expand and I'll iterate.
