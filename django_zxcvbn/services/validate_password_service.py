from django.conf import settings
from zxcvbn import zxcvbn


class ValidatePasswordService(object):

    def __init__(self, password):
        self.min_length = getattr(settings, 'PASSWORD_MINIMUM_LENGTH', -1)
        self.min_strength = getattr(settings, 'PASSWORD_MINIMUM_SCORE', -1)
        self.password = password

    def call(self):
        if self.password is None or not self.password.strip():
            return self._serialize_results({
                'score': 0,
                'feedback': {'suggestions': [
                    'The minimum length is {}'.format(self.min_length)
                ]}})

        if len(self.password) < self.min_length:
            return self._serialize_results({
                'score': 0,
                'feedback': {'suggestions': [
                    'The minimum length is {}'.format(self.min_length)
                ]}})

        results = zxcvbn(self.password)
        return self._serialize_results(results)

    def _serialize_results(self, results):
        valid = results['score'] >= self.min_strength
        results.pop('calc_time', None)
        results.pop('guesses_log10', None)
        results.pop('crack_times_seconds', None)
        results.pop('sequence', None)

        return {
            'valid': valid,
            'min_length': self.min_length,
            'min_strength': self.min_strength,
            'results': results
        }
