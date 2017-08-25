# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool

from .utils import get_country_from_request
from djangocms_personalisation.cms_plugins import PersonaliseByPluginBase

from .models import PersonaliseByCountryPluginModel


class PersonaliseByCountryPlugin(PersonaliseByPluginBase):
    """
    This plugin allows personalisation based on the visitor's country code.
    Use of this requires a header with the county code to be provided.
    Either through an upstream proxy or by a middleware.
    """

    model = PersonaliseByCountryPluginModel

    name = _('by country')

    #
    # If django-easy-select2 is installed, we can greatly enhance the
    # useability of this change form.
    #
    try:
        from easy_select2 import select2_modelform
        form = select2_modelform(
            PersonaliseByCountryPluginModel,
            attrs={'width': '250px'}
        )
    except ImportError:
        pass

    def is_context_appropriate(self, context, instance):
        request = context.get('request')
        if request:
            code = get_country_from_request(request)
        else:
            code = None

        return (code == instance.country_code)

plugin_pool.register_plugin(PersonaliseByCountryPlugin)
