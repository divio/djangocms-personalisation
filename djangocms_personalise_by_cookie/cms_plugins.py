# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool

from djangocms_personalisation.cms_plugins import PersonaliseByPluginBase
from .models import PersonaliseByCookiePluginModel


class PersonaliseByCookiePlugin(PersonaliseByPluginBase):
    """
    This is a segmentation plugin that renders output on the condition that a
    cookie with ``cookie_key`` is present and has the value ``cookie_value``.
    """

    model = PersonaliseByCookiePluginModel
    name = _('by cookie')

    def is_context_appropriate(self, context, instance):
        request = context.get('request')
        value = request.COOKIES.get(instance.cookie_key)
        return value == instance.cookie_value

plugin_pool.register_plugin(PersonaliseByCookiePlugin)
