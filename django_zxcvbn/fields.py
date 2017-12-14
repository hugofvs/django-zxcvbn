from django.forms import CharField

from django_zxcvbn_field.validators import ZXCVBNValidator
from django_zxcvbn_field.widgets import PasswordStrengthInput


class PasswordField(CharField):
    default_validators = [ZXCVBNValidator()]

    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 128

        if "widget" not in kwargs:
            kwargs["widget"] = PasswordStrengthInput(render_value=False)

        super(PasswordField, self).__init__(*args, **kwargs)
