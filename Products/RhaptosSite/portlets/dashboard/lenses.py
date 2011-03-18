# -*- coding: utf-8 -*-
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implements

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base
from Products.RhaptosSite import RhaptosMessageFactory as _


class ILensePortlet(IPortletDataProvider):
    """Portlet for lense creation and inspection."""


class Assignment(base.Assignment):
    implements(ILensePortlet)

    @property
    def title(self):
        return _(u"Create and edit content")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('lenses.pt')

    title = _('portlet_access_lenses',
              default=u"Access lenses")


class AddForm(base.NullAddForm):
    form_fields = form.Fields(ILensePortlet)
    label = _(u"Add Rhaptos Lense Portlet")
    description = _(u"A Rhaptos portlet that gives the user an easy way to "
                    "create and inspect lenses.")

    def create(self):
        return Assignment()
