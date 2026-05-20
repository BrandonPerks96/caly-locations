from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager, LowercaseEmailField

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = LowercaseEmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'), 
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        _('active'), 
        default=True,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    )
    is_external = models.BooleanField(
        _('external'), 
        default=False,
        help_text=_('Designates whether this user should be treated as an external user.')
    )
    created = models.DateTimeField(editable=False, auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name or self.email

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name or self.email

    def has_perm(self, perm, obj=None):
        """User has a specific permission."""
        return True

    def has_module_perms(self, app_label):
        """User has permissions to view the app `app_label`."""
        return True
