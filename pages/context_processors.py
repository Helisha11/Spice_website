from django.conf import settings


def branding_config(request):
    """Injects BRANDING_CONFIG from settings into all templates.

    Returns a dict with key `BRANDING_CONFIG` which is the parsed JSON from
    `config.json` (loaded into settings at startup).
    """
    return {
        'BRANDING_CONFIG': getattr(settings, 'BRANDING_CONFIG', {}),
    }


def cart_count(request):
    cart = request.session.get('cart', {})
    total = sum(cart.values()) if isinstance(cart, dict) else 0
    return {'cart_count': total}
