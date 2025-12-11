# users/validators.py

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PasswordComplexityValidator:
    """
    Validateur qui exige la présence de :
    - au moins une lettre minuscule
    - au moins une lettre majuscule
    - au moins un chiffre
    - au moins un caractère spécial
    """
    def validate(self, password, user=None):
        errors = []
        if not re.search('[a-z]', password):
            errors.append(ValidationError(
                _("Le mot de passe doit contenir au moins une lettre minuscule."),
                code='password_no_lowercase'
            ))
        if not re.search('[A-Z]', password):
            errors.append(ValidationError(
                _("Le mot de passe doit contenir au moins une lettre majuscule."),
                code='password_no_uppercase'
            ))
        if not re.search('[0-9]', password):
            errors.append(ValidationError(
                _("Le mot de passe doit contenir au moins un chiffre."),
                code='password_no_digit'
            ))
        if not re.search('[!@#$%^&*(),.?":{}|<>]', password):
            errors.append(ValidationError(
                _("Le mot de passe doit contenir au moins un caractère spécial "
                  '(!@#$%^&*(),.?":{}|<>).'),
                code='password_no_symbol'
            ))
        
        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return _(
            "Votre mot de passe doit contenir au moins une majuscule, "
            "une minuscule, un chiffre et un caractère spécial."
        )