# -*- coding: utf-8 -*-
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implements

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base
from Products.RhaptosSite import RhaptosMessageFactory as _


class IContentPortlet(IPortletDataProvider):
    """Portlet about creating, editing and finding content."""


class Assignment(base.Assignment):
    implements(IContentPortlet)

    @property
    def title(self):
        return _(u"Create and edit content")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('content.pt')

    title = _('portlet_create_and_edit_content',
              default=u"Create and edit content")


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IContentPortlet)
    label = _(u"Add Rhaptos Content Portlet")
    description = _(u"A Rhaptos portlet that gives the user an easy way to "
                    "create, edit and search for content.")

    def create(self):
        return Assignment()
