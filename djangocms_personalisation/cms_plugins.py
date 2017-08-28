# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import PersonalisePluginModel, PersonaliseFallbackPluginModel, \
    PersonalisationRedirectPluginModel


class PersonaliseByPluginBase(CMSPluginBase):
    """
    Abstract base class to be used for all segment plugins. It provides the
    default implementation of necessary additional methods for:

        * Registering conditions for Segmentation Previews for operators;
        * Reporting if the segment's condition(s) are met.

    Also, by using this base class, the Segmentation Group Plugin will be able
    accept the plugin (The Segmentation Group plugin has child_classes set to
    this class).
    """

    class Meta:
        abstract = True

    allow_children = True
    cache = False
    module = _('Personalisation')
    parent_classes = ['PersonalisePlugin', ]
    render_template = 'djangocms_personalisation/_segment.html'
    text_enabled = False

    #
    # Leave set to True to allow this plugin to be displayed in the Segment
    # Toolbar Menu for overriding by the operator.
    #
    allow_overrides = True

    def get_segment_override(self, context, instance):
        """
        If the current user is logged-in and this segment plugin allows
        overrides, then return the current override for this segment, else,
        returns Override.NoOverride.

        This should NOT be overridden in subclasses.
        """

        # This can't be defined at the file level, else circular imports
        from .segment_pool import segment_pool, SegmentOverride

        request = context['request']
        if request.user.is_authenticated():
            return segment_pool.get_override_for_segment(
                request.user, self, instance
            )

        return SegmentOverride.NoOverride

    def is_context_appropriate(self, context, instance):
        """
        Return True if this plugin is appropriate for rendering in the given
        context. (Non-degenerate) Segment Plugins should override this and
        supply the appropriate tests.
        """

        return True


class PersonalisePlugin(PersonaliseByPluginBase):
    """
    This is a special SegmentPlugin that acts as a top-level container for
    segmentation plugins and can set an upper-limit to the number of children
    that will be rendered in the current context.
    """

    allow_children = True
    model = PersonalisePluginModel
    module = _('Personalisation')
    name = _('Personalise')
    parent_classes = None
    render_template = 'djangocms_personalisation/_personalise.html'

    allow_overrides = False

    fieldsets = (
        (None, {
            'fields': ('label',),
        }),
        (_('Advanced'), {
            'fields': ('max_children',),
            'classes': ('collapse',),
        }),
    )

    def render(self, context, instance, placeholder):
        context = super(PersonalisePlugin, self).render(
            context, instance, placeholder)
        context['child_plugins'] = self.get_context_appropriate_children(
            context, instance)
        return context

    @classmethod
    def get_child_plugin_candidates(cls, slot, page):
        """
        Returns a list of all plugin classes
        that will be considered when fetching
        all available child classes for this plugin.
        """
        # Adding this as a separate method,
        # we allow other plugins to affect
        # the list of child plugin candidates.
        # Useful in cases like djangocms-text-ckeditor
        # where only text only plugins are allowed.
        from cms.plugin_pool import plugin_pool

        return [
            plugin for plugin
            in plugin_pool.registered_plugins
            if issubclass(plugin, PersonaliseByPluginBase)
        ]

    def is_context_appropriate(self, context, instance):
        """
        Returns True if any of its children are context-appropriate,
        else False.
        """
        apt_children = self.get_context_appropriate_children(context, instance)
        num_apt = sum( 1 for child in apt_children if child[1] )
        return num_apt > 0

    def get_context_appropriate_children(self, context, instance):
        from .segment_pool import SegmentOverride
        """
        Returns a LIST OF TUPLES each containing a child plugin instance and a
        Boolean representing the plugin's appropriateness for rendering in
        this context.
        """

        children = []
        # child_plugin_instances can sometimes be None
        generic_children = instance.child_plugin_instances or []
        render_all = (instance.max_children == 0)
        slots_remaining = instance.max_children

        for child_instance in generic_children:

            child_plugin = child_instance.get_plugin_class_instance()

            if child_plugin.model != child_instance.__class__:
                # If the child_instance's class does NOT
                # equal the registered plugin's model
                # then we're dealing with an orphan plugin.
                continue

            if render_all or slots_remaining > 0:

                if hasattr(child_plugin, 'is_context_appropriate'):
                    #
                    # This quacks like a segment plugin...
                    #
                    if (hasattr(child_plugin, 'allow_overrides') and
                            child_plugin.allow_overrides and
                            hasattr(child_plugin, 'get_segment_override')):

                        override = child_plugin.get_segment_override(
                            context, child_instance)

                        if override == SegmentOverride.ForcedActive:
                            child = (child_instance, True)
                        elif override == SegmentOverride.ForcedInactive:
                            child = (child_instance, False)
                        else:
                            #
                            # There's no override, so, just let the segment
                            # decide...
                            #
                            child = (
                                child_instance,
                                child_plugin.is_context_appropriate(
                                    context, child_instance
                                ),
                            )
                    else:
                        #
                        # Hmmm, this segment plugin appears to have no
                        # allow_overrides property or get_segment_override()
                        # method. OK then, let the plugin decide if it is
                        # appropriate to render.
                        #
                        child = (
                            child_instance,
                            child_plugin.is_context_appropriate(
                                context, child_instance
                            ),
                        )
                else:
                    #
                    # This doesn't quack like a Segment Plugin, so, it is
                    # always OK to render.
                    #
                    child = (child_instance, True,)

                if child[1]:
                    slots_remaining -= 1
            else:
                #
                # We've run out of available slots...
                #
                child = (child_instance, False,)

            children.append(child)

        return children


class PersonaliseFallbackPlugin(PersonaliseByPluginBase):
    """
    This PersonaliseBy plugin is for the Fallback case and always matches.
    """

    model = PersonaliseFallbackPluginModel
    name = _('Fallback')

    # It doesn't make much sense to override this one...
    allow_overrides = False

    def is_context_appropriate(self, context, instance):
        return True


class PersonalisationRedirectPlugin(CMSPluginBase):
    model = PersonalisationRedirectPluginModel
    name = _('Redirect To')
    render_template = 'djangocms_personalisation/redirect.html'


plugin_pool.register_plugin(PersonalisePlugin)
plugin_pool.register_plugin(PersonaliseFallbackPlugin)
plugin_pool.register_plugin(PersonalisationRedirectPlugin)
