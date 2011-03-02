# -*- coding: utf-8 -*-
"""
Rhaptos notes
-------------

- Custom registration schema (IRhaptosRegistrationSchema)

"""
from zope.interface import Interface
from zope import schema
from zope.formlib import form
from plone.app.users.browser import register

from Products.RhaptosSite import RhaptosMessageFactory as _


class IRhaptosRegistrationSchema(Interface):
    """See the base registration for the inherited schema fields"""

    # TODO: Do we want to keep the fullname (provided by default) or enable
    #       two separate fields: first name and last name? 
    ##first_name = 
    ##last_name = 
    home_page = schema.ASCIILine(
        title=_(u'lable_user_home_page', default=u'Home Page'),
        description=_(u'help_user_home_page',
                      default=u"Enter the address of your personal Web "
                               "page e.g. http://www.jdoe.com/~jdoe/"),
        required=False,)
    site_license_agreement = schema.Bool(
        title=_(u'site_license_agreement',
                # TODO: Link to the Connexions Site License
                default=u"I have read the Connexions Site License and I agree to be bound by its terms"),
        default=False)


class RegistrationForm(register.RegistrationForm):
    """Rhaptos Override of plone.app.users.browser.register.RegistrationForm
    to provide additional user information."""

    @property
    def form_fields(self):
        """Add our custom form fields to the dynamically created list of
        form fields."""
        form_fields = super(RegistrationForm, self).form_fields
        #: Add our fields to the mix.
        form_fields += form.Fields(IRhaptosRegistrationSchema)
        return form_fields


class AddUserForm(register.BaseRegistrationForm):
    """Rhaptos Override of plone.app.users.browser.register.AddUserForm
    to enable additional user information."""

