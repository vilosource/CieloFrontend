"""
Context processors for CieloFrontend
"""
from django.conf import settings


def api_urls(request):
    """
    Make API URLs available to all templates.
    
    This context processor makes the IDENTITY_API_URL and BILLING_API_URL
    settings available to all templates as template variables.
    """
    return {
        'IDENTITY_API_URL': getattr(settings, 'IDENTITY_API_URL', 'https://identity.dev.viloforge.com'),
        'BILLING_API_URL': getattr(settings, 'BILLING_API_URL', 'https://billing.dev.viloforge.com'),
    }
