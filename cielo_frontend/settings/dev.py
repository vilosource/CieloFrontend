from .base import *
import os

DEBUG = True

SESSION_COOKIE_DOMAIN = ".cielo.test"
SESSION_COOKIE_PATH = "/"
ALLOWED_HOSTS = [".cielo.test", "localhost"]

# Backend API URLs
IDENTITY_API_URL = os.getenv("IDENTITY_API_URL", "http://identity.cielo.test")
BILLING_API_URL = os.getenv("BILLING_API_URL", "http://billing.cielo.test")
