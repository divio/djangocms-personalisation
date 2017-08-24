# -*- coding: utf-8 -*-
from aldryn_client import forms


class Form(forms.BaseForm):

    def to_settings(self, data, settings):
        settings['INSTALLED_APPS'].extend([
            'djangocms_personalisation',
            # TODO: make these configurable from the form
            'djangocms_personalise_by_auth',
            'djangocms_personalise_by_cookie',
            'djangocms_personalise_by_country',
            'djangocms_personalise_manually',
        ])
        return settings
