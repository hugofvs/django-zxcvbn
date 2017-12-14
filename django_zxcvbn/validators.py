from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django_zxcvbn_field.services.validate_password_service import (
    ValidatePasswordService)


class ZXCVBNValidator(object):
    """ZXCVBN validator."""

    code = 'password_too_weak'

    def __call__(self, value):
        """Call method, run self.validate (can be used in form fields)."""
        return self.validate(value)

    def validate(self, password, user=None):
        """Validate method, run zxcvbn and check score."""
        results = ValidatePasswordService(password).call()

        if not results['valid']:
            results_feedback = results['results'].get('feedback', {})
            feedback = ', '.join(results_feedback.get('suggestions', []))

            if not feedback:
                feedback = 'Use a more complex password'

            raise ValidationError(_(feedback), code=self.code, params={})

    def get_help_text(self):
        """Help text to print when ValidationError."""
        return u'Use a more complex password'
