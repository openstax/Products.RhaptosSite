# -*- coding: utf-8 -*-
"""
Rhaptos notes
-------------

- Custom registration schema (IRhaptosRegistrationSchema)

We should look into doing the registration fields as a single override of
the UserDataSchema. Then modifying the membership registration fields
(visable at /@@member-registration). I believe these pieces could be done
using GenericSetup. [pumazi]

"""
from zope.interface import Interface
from zope import schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib import form
from zope.formlib.interfaces import WidgetInputError
from plone.app.users.browser import register

from Products.RhaptosSite import RhaptosMessageFactory as _


class IRhaptosRegistrationSchema(Interface):
    """See the base registration for the inherited schema fields"""

    # TODO: Do we want to keep the fullname (provided by default) or enable
    #       two separate fields: first name and last name? 
    ##first_name = 
    ##last_name = 
    home_page = schema.URI(
        title=_(u'lable_user_home_page', default=u'Home page'),
        description=_(u'help_user_home_page',
                      default=u"Enter the address of your personal Web "
                              "page e.g. http://www.jdoe.com/~jdoe/"),
        required=False,
        )
    site_license_agreement = schema.Bool(
        title=_(u'site_license_agreement',
                # FIXME: Hard-coded value to a site license that doesn't exist.
                default=u"I have read the <a href=\"/sitelicense\">"
                        "Connexions Site License</a> and I "
                        "agree to be bound by its terms"),
        required=True,
        )


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

    # Actions validators
    def validate_registration(self, action, data):
        """Specific business logic for this registration (join) form."""
        errors = super(RegistrationForm, self).validate_registration(action,
                                                                     data)
        # Note: Validation for the home page field is done in the super class.

        #: Validate the site license agreement field.
        # FIXME: Currently this error does not display correctly. The status
        #        message will appear at the top of the page but the field will
        #        not highlight. 
        site_license_agreement = self.widgets['site_license_agreement']
        if site_license_agreement.getInputValue() is not True:
            err_str = _('msg_has_not_agreed_to_site_license',
                        default=u"You must agree to the terms of service "
                                "in the Connexions site license.")
            #: Note: CheckBoxWidget widget doesn't have a label for stylistic
            #  reasons, but we need it for the form validation.
            errors.append(WidgetInputError(site_license_agreement.name,
                                           site_license_agreement.name,
                                           err_str))
        return errors


class AddUserForm(register.BaseRegistrationForm):
    """Rhaptos Override of plone.app.users.browser.register.AddUserForm
    to enable additional user information."""
    template = ViewPageTemplateFile('templates/rhaptos-newuser_form.pt')
