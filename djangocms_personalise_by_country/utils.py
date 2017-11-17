# -*- coding: utf-8 -*-
from django.conf import settings
from .constants import DEFAULT_COUNTRY_HEADERS


def get_country_from_request(request, headers=None):
    if headers is None:
        headers = getattr(
            settings,
            'DJANGOCMS_PERSONALISE_BY_COUNTRY_HEADERS',
            DEFAULT_COUNTRY_HEADERS
        )
    for header in headers:
        country_code = request.META.get(header)
        if country_code:
            return country_code
    return None
