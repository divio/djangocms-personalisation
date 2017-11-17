# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url
from django.contrib import admin

from .models import Personalisation
from .views import set_override, reset_all_overrides


class PersonalisationAdmin(admin.ModelAdmin):

    #
    # Note: model.Personalisation is empty and un-managed. Its sole purpose is
    # to provide the opportunity to add custom views to the AdminSite for
    # managing segments from the toolbar.
    #

    def get_model_perms(self, request):
        """
        Returns an empty perms dict which has the effect of disabling its
        display in the AdminSite, but still allows access to the views defined
        below.
        """
        return dict()

    def get_urls(self):

        return [
            url(r'set_override/$',
                self.admin_site.admin_view(set_override),
                name='djangocms_personalisation_set_override'
                ),

            url(r'reset_all_overrides/$',
                self.admin_site.admin_view(reset_all_overrides),
                name='djangocms_personalisation_reset_all_overrides'
                ),
        ] + super(PersonalisationAdmin, self).get_urls()


admin.site.register(Personalisation, PersonalisationAdmin)
