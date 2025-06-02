from .base import *
import os

DEBUG = True

SESSION_COOKIE_DOMAIN = ".cielo.test"
SESSION_COOKIE_PATH = "/"
ALLOWED_HOSTS = [".cielo.test", "localhost", "127.0.0.1"]

# Backend API URLs
IDENTITY_API_URL = os.getenv("IDENTITY_API_URL", "http://identity.cielo.test")
BILLING_API_URL = os.getenv("BILLING_API_URL", "http://billing.cielo.test")

# Django Debug Toolbar
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'debug_toolbar'] + ['debug_toolbar']
INTERNAL_IPS = ['127.0.0.1']
MIDDLEWARE = [middleware for middleware in MIDDLEWARE if middleware != 'debug_toolbar.middleware.DebugToolbarMiddleware'] + ['debug_toolbar.middleware.DebugToolbarMiddleware']
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}


print("Development settings loaded.")
print("Debug mode is ON.")
print(f"Identity API URL: {IDENTITY_API_URL}")
print(f"Billing API URL: {BILLING_API_URL}")
# Static files (CSS, JavaScript, Images)
print("Static files will be served from the 'static' directory.")
print(f"Templates will be loaded from: {TEMPLATES[0]['DIRS']}")