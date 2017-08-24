# -*- coding: utf-8 -*-
from aldryn_client import forms


class Form(forms.BaseForm):

    def to_settings(self, data, settings):
        settings['INSTALLED_APPS'].extend([
            'djangocms_segmentation',
            # TODO: make these configurable from the form
            'djangocms_segment_by_auth',
            'djangocms_segment_by_cookie',
            'djangocms_segment_by_country',
            'djangocms_segment_by_switch',
        ])
        return settings
