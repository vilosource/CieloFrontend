from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Create a default admin user if no superuser exists'

    def handle(self, *args, **options):
        # Check if any superuser exists
        if not User.objects.filter(is_superuser=True).exists():
            try:
                # Create default admin user
                admin_user = User.objects.create_superuser(
                    username='admin',
                    email='admin@cielo.local',
                    password='admin'
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created default admin user: {admin_user.username}'
                    )
                )
                self.stdout.write(
                    self.style.WARNING(
                        'Default credentials - Username: admin, Password: admin'
                    )
                )
                self.stdout.write(
                    self.style.WARNING(
                        'Please change the default password for security!'
                    )
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR(
                        'Admin user already exists or there was an error creating it.'
                    )
                )
        else:
            self.stdout.write(
                self.style.SUCCESS('Superuser already exists. No action needed.')
            )
