from django.conf.urls import patterns, url
from django_zxcvbn_field.views import zxcvbn_validator_view

urlpatterns = patterns(
    '',
    url(r'zxcvbn_validator/$', zxcvbn_validator_view,
        name='zxcvbn_validator'),
)
