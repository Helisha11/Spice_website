from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, FAQ, VisitorRegistration, ContactMessage
from .forms import ContactForm, VisitorRegistrationForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import json
from pathlib import Path


def home(request):
    featured = Product.objects.filter(is_active=True)[:4]
    context = {
        'reg_form': VisitorRegistrationForm(),
        'featured': featured,
    }
    return render(request, 'pages/home.html', context)


def get_admin_contact():
    """Load admin email and phone from config.json"""
    try:
        config_path = Path(settings.BASE_DIR) / 'config.json'
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get('email'), config.get('phone')
    except Exception as e:
        print(f"Error loading config: {e}")
        return None, None


def register(request):
    if request.method == 'POST':
        form = VisitorRegistrationForm(request.POST)
        if form.is_valid():
            # Save the registration
            visitor = form.save()
            
            # Get admin email from settings
            admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
            
            # Send email to admin
            if admin_email:
                subject = f"New Registration Inquiry: {form.cleaned_data['name']}"
                message = f"""
New visitor registration received from the website:

Name: {form.cleaned_data['name']}
Email: {form.cleaned_data['email']}
Phone: {form.cleaned_data['phone']}
Company: {form.cleaned_data.get('company', 'N/A')}
Country: {form.cleaned_data.get('country', 'N/A')}
Message: 
{form.cleaned_data.get('message', 'No additional message.')}

Registered at: {visitor.created_at}
"""
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [admin_email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"=== REGISTRATION EMAIL ERROR ===")
                    print(f"Error sending registration email: {type(e).__name__}: {e}")
                    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
                    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
                    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
                    print(f"To: {admin_email}")
                    print(f"=================================")
            
            messages.success(request, 'Thanks for registering!')
            return redirect('home')
        else:
            # Preserve errors and show on home modal
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")
            return redirect('home')
    return redirect('home')


def products(request):
    sel = request.GET.get('category')
    qs = Product.objects.filter(is_active=True)
    # Exclude specific products from public listing
    excluded_names = [
        "Ground Cardamom",
        "Bay Leaf",
        "Whole All Spices",
        "Card",
    ]
    qs = qs.exclude(name__in=excluded_names)
    if sel:
        qs = qs.filter(category=sel)
    categories = [c for c, _ in Product.CATEGORY_CHOICES]
    context = {
        'items': qs,
        'categories': categories,
        'selected': sel or '',
    }
    return render(request, 'pages/products.html', context)


def product_detail(request, slug: str):
    from django.shortcuts import get_object_or_404
    p = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(is_active=True, category=p.category).exclude(id=p.id)[:3]
    return render(request, 'pages/product_detail.html', {'p': p, 'related': related})


def services(request):
    return render(request, 'pages/services.html')


def faq(request):
    items = FAQ.objects.filter(is_active=True)
    return render(request, 'pages/faq.html', {'items': items})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save contact message to database
            contact_msg = ContactMessage.objects.create(**form.cleaned_data)
            
            # Get admin email from settings
            admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
            
            # Send email to admin
            if admin_email:
                subject = f"New Contact Message: {form.cleaned_data['name']}"
                message = f"""
You have received a new message from the contact form:

Name: {form.cleaned_data['name']}
Email: {form.cleaned_data['email']}
Phone: {form.cleaned_data['phone']}
Message: 
{form.cleaned_data['message']}

Sent at: {contact_msg.created_at}
"""
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [admin_email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Your message was sent successfully!')
                except Exception as e:
                    print(f"=== EMAIL ERROR ===")
                    print(f"Error sending email: {type(e).__name__}: {e}")
                    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
                    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
                    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
                    print(f"To: {admin_email}")
                    print(f"===================")
                    messages.warning(request, 'Message saved but email notification failed.')
                return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})


def add_to_cart(request, product_id:int):
    """Simple session-based add-to-cart (increments qty)."""
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    # redirect back to products page or referer
    referer = request.META.get('HTTP_REFERER') or reverse('products')
    return HttpResponseRedirect(referer)


def remove_from_cart(request, product_id:int):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return HttpResponseRedirect(reverse('cart'))


def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(pk=int(pid))
        except Product.DoesNotExist:
            continue
        price = p.price or 0
        subtotal = price * qty if price else 0
        items.append({'product': p, 'qty': qty, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'pages/cart.html', {'items': items, 'total': total})
