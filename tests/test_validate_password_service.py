from django.test import TestCase
from django_zxcvbn.services import ValidatePasswordService


class ValidatePasswordServiceTestCase(TestCase):
    def test_init_method(self):
        password = '1234'
        service = ValidatePasswordService(password)
        self.assertEqual(service.password, password)
        self.assertEqual(service.min_length, 8)
        self.assertEqual(service.min_strength, 3)

    def test_empty_password(self):
        password = None
        result = ValidatePasswordService(password).call()
        expected_result = {
            'min_length': 8,
            'min_strength': 3,
            'results': {
                'feedback': {'suggestions': ['The minimum length is 8']},
                'score': 0
            },
            'valid': False}
        self.assertDictEqual(result, expected_result)

    def test_minimum_length(self):
        password = '12345'
        result = ValidatePasswordService(password).call()
        expected_result = {
            'min_length': 8,
            'min_strength': 3,
            'results': {
                'feedback': {'suggestions': ['The minimum length is 8']},
                'score': 0
            },
            'valid': False}
        self.assertDictEqual(result, expected_result)

    def test_weak_password(self):
        password = '12345678'
        result = ValidatePasswordService(password).call()
        expected_result = {
            'min_length': 8,
            'min_strength': 3,
            'results': {
                'feedback': {
                    'suggestions': ['Add another word or two. '
                                    'Uncommon words are better.'],
                    'warning': 'This is a top-10 common password.'
                },
                'password': password,
                'score': 0
            },
            'valid': False}

        self.assertDictEqual(result, expected_result)

    def test_strong_password(self):
        password = 'this is just a test password'
        result = ValidatePasswordService(password).call()
        expected_result = {
            'min_length': 8,
            'min_strength': 3,
            'results': {
                'feedback': {'suggestions': [], 'warning': ''},
                'password': password,
                'score': 4
            },
            'valid': True}

        self.assertDictEqual(result, expected_result)
