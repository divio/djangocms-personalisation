# -*- coding: utf-8 -*-
from django.conf import settings


DEFAULT_COUNTRY_HEADERS = [
    'COUNTRY_CODE',
    'CF-IPCOUNTRY',  # CloudFlare
]


def get_country_from_request(request, headers=None):
    if headers is None:
        headers = getattr(
            settings,
            'DJANGOCMS_SEGMENT_BY_COUNTRY_HEADERS',
            DEFAULT_COUNTRY_HEADERS
        )
    for header in headers:
        country_code = request.META.get(header)
        if country_code:
            print "COUNTRY CODE {}".format(country_code)
            return country_code
    print "COUNTRY CODE NONE"
    return None
