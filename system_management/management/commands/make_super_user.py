import os
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.contrib.auth.password_validation import validate_password
from dotenv import load_dotenv

load_dotenv('./.env')

class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Handles the logic for creating a new superuser with specific attributes.
        """
        required_vars = ['SUPER_USER_EMAIL', 'SUPER_USER_PASSWORD', 'SUPER_USER_FIRST_NAME', 'SUPER_USER_LAST_NAME']
        
        for var in required_vars:
            if not os.getenv(var):
                self.stderr.write(self.style.ERROR(f'Missing environment variable: {var}'))
                return
        
        email = os.environ['SUPER_USER_EMAIL']
        password = os.getenv('SUPER_USER_PASSWORD')
        User = get_user_model()

        try:
            validate_password(password)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Invalid password: {e}'))
            return
        
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=password,
                first_name=os.getenv('SUPER_USER_FIRST_NAME'),
                last_name=os.getenv('SUPER_USER_LAST_NAME'),
                phone=os.getenv('SUPER_USER_PHONE_NUMBER', '1234567890'),
                is_confirmed=True,
                is_active=True,
                is_external=False,
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))