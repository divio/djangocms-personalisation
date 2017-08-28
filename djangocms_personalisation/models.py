# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.translation import ugettext_lazy as _, string_concat

from cms.models import CMSPlugin


#
# NOTE: The PersonalisePluginModel does NOT subclass PersonaliseByPluginBaseModel
#
@python_2_unicode_compatible
class PersonalisePluginModel(CMSPlugin):

    #
    # Need to consider how best to display this in the Plugin Change Form...
    #
    #   0 means "Display ALL matches",
    #   1 means "Display first match",
    #   2 means "Display up to two matches,"
    #     and so on...
    #

    label = models.CharField(
        _('label'),
        blank=True,
        default='',
        help_text=_('Optionally set a label for this limit block.'),
        max_length=128,
    )

    max_children = models.PositiveIntegerField(
        _('# of matches to display'),
        blank=False,
        default=1,
        help_text=_('Display up to this amount of matches?'),
    )

    @property
    def configuration_string(self):
        if self.max_children == 0:
            return _('Show All')
        elif self.max_children == 1:
            return _('Show First')
        else:
            return string_concat(_('Show First'), ' ', self.max_children)

    def __str__(self):
        """
        If there is a label, show that with the configuration in brackets,
        otherwise, just return the configuration string.
        """

        if self.label:
            conf_str = _('{label} [{config}]').format(
                label=self.label,
                config=force_text(self.configuration_string),
            )
        else:
            conf_str = self.configuration_string

        return force_text(conf_str)


@python_2_unicode_compatible
class PersonaliseByPluginBaseModel(CMSPlugin):
    """
    Defines a common interface for PersonaliseBy plugins. Also note that plugin
    model's subclassing this class will automatically be (un-)registered
    (from)to the pool via 'pre_delete' and 'post_save' signals. This
    is implemented in djangocms_personalisation.segment_pool.
    """

    class Meta:
        abstract = True

    label = models.CharField(
        _('label'),
        blank=True,
        default='',
        max_length=128,
    )

    @property
    def configuration_string(self):
        """
        Return a ugettext_lazy object (or a lazy function that returns the
        same) that represents the configuration for the plugin instance in a
        unique, concise manner that is suitable for a toolbar menu option.

        Some Examples:
            Cookie:
                '"key" equals "value"'
            Country:
                'Country is Kenya'
            Auth:
                'User is authenticated'
            Switch:
                'Always ON'
            Limit:
                'Show First'

        In cases where the returned string is composed with placeholders, E.g.:

            Cookie:
                ugettext_lazy('“{key}” equals “{value}”').format(
                    key=self.key,
                    value=self.value
                )

        You *must* actually return a evaluated, lazy wrapper around the
        gettext_lazy operation as follows:

            def configuration_string(self):
                wrapper():
                    return ugettext_lazy('“{key}” equals “{value}”').format(
                        key=self.key,
                        value=self.value
                    )

                # NOTE: the trailing '()'
                return lazy(wrapper, six.text_type)()

        Otherwise, the translations won't happen.

        This construction is not required for untranslated or non-
        parameterized translations.


        NOTE: Each subclass must override to suit.
        """
        raise NotImplementedError("Please Implement this method")

    def __str__(self):
        """
        If there is a label, show that with the configuration in brackets,
        otherwise, just return the configuration string.
        """

        if self.label:
            conf_str = _('{label} [{config}]').format(
                label=self.label,
                config=force_text(self.configuration_string),
            )
        else:
            conf_str = self.configuration_string

        return force_text(conf_str)


class PersonaliseFallbackPluginModel(PersonaliseByPluginBaseModel):
    @property
    def configuration_string(self):
        return ''


@python_2_unicode_compatible
class PersonalisationRedirectPluginModel(CMSPlugin):
    label = models.CharField(
        _('label'),
        blank=True,
        default='',
        max_length=128,
    )
    # TODO: Also allow redirecting to a CMS Page and/or relative URLs?
    redirect_to = models.URLField(
        _('redirect to'),
        max_length=2083,
    )
    delay = models.PositiveSmallIntegerField(
        _('delay before redirect'),
        default=0,
    )

    def __str__(self):
        """
        If there is a label, show that with the configuration in brackets,
        otherwise, just return the configuration string.
        """

        if self.label:
            conf_str = _('{label} [{config}]').format(
                label=self.label,
                config=force_text(self.redirect_to),
            )
        else:
            conf_str = self.redirect_to

        return force_text(conf_str)


@python_2_unicode_compatible
class Personalisation(models.Model):
    """
    This is a hollow, unmanaged model that simply allows us to attach custom
    admin views into the AdminSite.
    """

    class Meta:
        managed = False

    def __str__(self):
        return 'Personalisation is an empty, unmanaged model.'

