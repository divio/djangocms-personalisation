# -*- coding: utf-8 -*-
from aldryn_client import forms


class Form(forms.BaseForm):
    enable_djangocms_personalise_by_auth = forms.CheckboxField(
        'Enable Personalise by Auth',
        required=False,
        initial=True,
    )
    enable_djangocms_personalise_by_cookie = forms.CheckboxField(
        'Enable Personalise by Cookie',
        required=False,
        initial=True,
    )
    enable_djangocms_personalise_by_country = forms.CheckboxField(
        'Enable Personalise by Country',
        required=False,
        initial=True,
        help_text=(
            'Requires the country code to be provided as an http header. Works '
            'automatically with CloudFlare. Please contact support for more '
            'information.'
        )
    )
    enable_djangocms_personalise_by_parameters = forms.CheckboxField(
        'Enable Personalise by Parameters',
        required=False,
        initial=True,
    )
    enable_djangocms_personalise_manually = forms.CheckboxField(
        'Enable Personalise Manually',
        required=False,
        initial=True,
    )

    def to_settings(self, data, settings):
        from djangocms_personalise_by_country.constants import DEFAULT_COUNTRY_HEADERS
        from functools import partial
        from aldryn_addons.utils import djsenv
        env = partial(djsenv, settings=settings)

        settings['INSTALLED_APPS'].append('djangocms_personalisation')

        for key, value in data.items():
            if not key.startswith('enable_djangocms_personalise_'):
                continue
            if not value:
                continue
            settings['INSTALLED_APPS'].append(
                key.replace('enable_', '')
            )
            if key == 'enable_djangocms_personalise_by_parameters':
                settings['INSTALLED_APPS'].append('djangocms_attributes_field')
            elif key == 'enable_djangocms_personalise_by_country':
                settings['DJANGOCMS_PERSONALISE_BY_COUNTRY_HEADERS'] = env(
                    'DJANGOCMS_PERSONALISE_BY_COUNTRY_HEADERS',
                    DEFAULT_COUNTRY_HEADERS
                )
        return settings
