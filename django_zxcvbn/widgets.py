from django.forms import PasswordInput
from django.utils.safestring import mark_safe


class PasswordStrengthInput(PasswordInput):
    """Form widget to show the user how strong his/her password is."""

    def render(self, name, value, attrs=None):
        """Widget render method."""
        strength_markup = u"""
            <div class="form-group zxcvbn-form-group">
                <div class="input-group zxcvbn-password-input-group">
                    <input type="password" class="form-control"
                           id="zxcvbn-password" name="{n}" />
                    <span class="input-group-addon masked"
                          title="Click here to show/hide password"
                          style="cursor: pointer;" id="zxcvbn-toggle-show">
                        <span class="glyphicon glyphicon-eye-open"></span>
                    </span>
                </div>

                <div class="input-group"><small>Choose a password.
                You can include numbers and symbols.</small></div>

                <div id="zxcvbn-progress" class="progress">
                    <div class="progress-bar" id="zxcvbn-strength"
                         role="progressbar" aria-valuemin="0"
                         aria-valuemax="100" aria-valuenow="0">
                        <span class="sr-only"></span>
                    </div>
                </div>

                <ul id="zxcvbn-messages"></ul>
            </div>
        """.format(n=name, v=value)

        try:
            self.attrs['class'] = '%s password_strength'.strip() % self.attrs['class']  # noqa
        except KeyError:
            self.attrs['class'] = 'password_strength'

        return mark_safe(strength_markup)

    class Media(object):
        js = ('js/django_zxcvbn_field.js',)
