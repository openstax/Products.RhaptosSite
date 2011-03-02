# -*- coding: utf-8 -*-
from plone.app.users.browser.register import (
    BaseRegistrationForm,
    RegistrationForm,
    )


class RhaptosRegistrationForm(RegistrationForm):
    """Rhaptos Override of plone.app.users.browser.register.RegistrationForm
    to provide additional user information."""


class RhaptosAddUserForm(BaseRegistrationForm):
    """Rhaptos Override of plone.app.users.browser.register.AddUserForm
    to enable additional user information."""

