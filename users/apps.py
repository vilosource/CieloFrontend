from django.apps import AppConfig
from django.core.management import call_command
from django.db.utils import OperationalError
import os


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # Only run this during normal server startup, not during migrations
        if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
            try:
                # Import here to avoid circular imports
                from django.contrib.auth.models import User
                
                # Check if database tables exist and if any superuser exists
                if User.objects.filter(is_superuser=True).exists():
                    pass  # Superuser already exists
                else:
                    # No superuser exists, create default admin
                    call_command('create_default_admin')
                    
            except OperationalError:
                # Database tables don't exist yet (during initial migrations)
                pass
            except Exception as e:
                # Handle any other exceptions silently during app loading
                pass
