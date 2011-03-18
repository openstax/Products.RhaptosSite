# -*- coding: utf-8 -*-
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implements

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base
from Products.RhaptosSite import RhaptosMessageFactory as _


class IGuidePortlet(IPortletDataProvider):
    """Portlet displaying information about guides and tutorials
    concerning the usage of this site."""


class Assignment(base.Assignment):
    implements(IGuidePortlet)

    @property
    def title(self):
        return _(u"Guides and Tutorials")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('guide.pt')

    title = _('portlet_guide',
              default=u"Guides and Tutorials")


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IGuidePortlet)
    label = _(u"Add Rhaptos Guide Portlet")
    description = _(u"A Rhaptos portlet that supplies the user with links to"
                    "guides and tuturials about this site.")

    def create(self):
        return Assignment()
