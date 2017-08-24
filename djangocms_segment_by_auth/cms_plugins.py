# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool

from djangocms_segmentation.cms_plugins import SegmentPluginBase
from .models import SegmentByAuthPluginModel


class AuthenticatedSegmentPlugin(SegmentPluginBase):
    """
    This plugin allows segmentation based on the authentication/authorization
    status of the visitor.
    """

    model = SegmentByAuthPluginModel
    name = _('Segment by auth')

    def is_context_appropriate(self, context, instance):
        request = context.get('request')
        return request and request.user and request.user.is_authenticated()


plugin_pool.register_plugin(AuthenticatedSegmentPlugin)
