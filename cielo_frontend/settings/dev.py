from .base import *
import os

DEBUG = True

# Session configuration to match Identity Provider
SESSION_COOKIE_DOMAIN = ".dev.viloforge.com"
SESSION_COOKIE_NAME = 'cielo_sessionid'  # Match Identity Provider
SESSION_COOKIE_PATH = "/"
SESSION_COOKIE_SAMESITE = 'None'  # None required for cross-origin HTTPS
SESSION_COOKIE_SECURE = True  # Required for HTTPS and SameSite=None
SESSION_COOKIE_HTTPONLY = False  # Allow JavaScript access for cross-origin
SESSION_SAVE_EVERY_REQUEST = True  # Ensure session persistence
SESSION_COOKIE_AGE = 86400  # 24 hours - match Identity Provider

ALLOWED_HOSTS = [".dev.viloforge.com", "localhost", "127.0.0.1"]

# Backend API URLs - Updated for HTTPS domains
IDENTITY_API_URL = os.getenv("IDENTITY_API_URL", "https://identity.dev.viloforge.com")
BILLING_API_URL = os.getenv("BILLING_API_URL", "https://billing.dev.viloforge.com")

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
print("Static files will be served from the 'static' directory.")
print(f"Templates will be loaded from: {TEMPLATES[0]['DIRS']}")
