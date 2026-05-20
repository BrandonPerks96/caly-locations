from django.core.exceptions import ValidationError
import re

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                "The password must contain at least one uppercase letter.",
                code='password_no_upper',
            )
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                "The password must contain at least one lowercase letter.",
                code='password_no_lower',
            )
        # Check for at least one digit
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                "The password must contain at least one digit.",
                code='password_no_digit',
            )

    def get_help_text(self):
        return "Your password must contain at least one uppercase letter, one lowercase letter, and one digit."