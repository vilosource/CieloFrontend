from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings

@receiver(post_migrate)
def create_dev_superuser(sender, **kwargs):

    if not settings.DEBUG:
        return  # Only do this in development

    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        print("Creating default admin user...")
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'  # Ensure password is set during creation
        )
