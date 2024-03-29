# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST
from django.utils.encoding import force_text

from .segment_pool import segment_pool


@require_POST
def set_override(request):
    """
    This view (re)sets an override on a specific segment.
    """

    segment_class = request.POST.get('segment_class', None)
    segment_config = request.POST.get('segment_config', None)
    override = request.POST.get('override', None)

    segment_pool.set_override(request.user, segment_class, segment_config, override)
    return HttpResponse(force_text(_('The segment override was successfully changed.')))


def reset_all_overrides(request):
    """
    This view resets all segment overrides in one go.
    """

    segment_pool.reset_all_overrides(request.user)
    return HttpResponse(force_text(_('The all segment override were successfully reset.')))
