from django.db import models
from django.contrib.auth.base_user import BaseUserManager
 
 
class LowercaseEmailField(models.EmailField):
    """
    Custom EmailField that automatically converts email addresses to lowercase before saving to the database.
    """
    def to_python(self, value):
        """
        Ensure that the email value is converted to lowercase when loading the field from the database.
        """
        value = super().to_python(value)  # Get the value from the parent class, which handles normalization
        return value.lower() if isinstance(value, str) else value
 
 
class CustomUserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifier for authentication,
    replacing the default username field.
    """
 
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # Explicitly specify using the database alias
        return user
 
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a Superuser with the email and password, ensuring they have full admin rights.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
 
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
