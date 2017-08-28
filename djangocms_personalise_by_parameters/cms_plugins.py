# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool

from djangocms_personalisation.cms_plugins import PersonaliseByPluginBase
from .models import PersonaliseByParametersPluginModel
from .utils import request_matches_parameters


class PersonaliseByParametersPlugin(PersonaliseByPluginBase):
    """
    This is a segmentation plugin that renders output on the condition that a
    cookie with ``cookie_key`` is present and has the value ``cookie_value``.
    """

    model = PersonaliseByParametersPluginModel
    name = _('by parameters')

    def is_context_appropriate(self, context, instance):
        request = context.get('request')
        return request_matches_parameters(request, instance.parameters)

plugin_pool.register_plugin(PersonaliseByParametersPlugin)
