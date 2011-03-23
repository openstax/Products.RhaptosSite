# -*- coding: utf-8 -*-
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implements

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.app.portlets.portlets import base
from Products.RhaptosSite import RhaptosMessageFactory as _


class IWorkspacePortlet(IPortletDataProvider):
    """Portlet for managing a users workspace."""


class Assignment(base.Assignment):
    implements(IWorkspacePortlet)

    @property
    def title(self):
        return _(u"Workspace")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('workspace.pt')

    title = _('portlet_workspace',
              default=u"Workspace")

    @property
    def user_home(self):
        portal_membership = getToolByName(self.context, 'portal_membership')
        return portal_membership.getHomeFolder()

    @property
    def lens_home(self):
        lens_tool = getToolByName(self.context, 'lens_tool')
        folder = lens_tool.getIndividualFolder(create=False)
        return folder

    def highlight(self):
        # note: order matters in some places, here.
        # 'editobj' for example, should stop any location highlights,
        # and does so by coming before them.
        # 'listcontent' is called in context of 'mydashboard', so it
        # comes before that.
        # and a few other. In other words, tread carefully.

        try:
            rhaptos_obj = self.context.nearestRhaptosObject()
        except AttributeError:
            rhaptos_obj = None
        url = self.request.URL

        if url.find('listcontent') >= 0:
            # Highlight by type: modules/collections
            section = []
            content_types = self.request.get('type', None)
            if 'Module' in content_types:
                section.append('module')
            if 'Collection' in content_types:
                section.append('collection')
            return 'bytype', section
        elif url.find('manageworkgroups') >= 0 \
             or url.find('create_workgroup') >= 0:
            # Highlight by location: special action
            return 'bylocationaction', 'workgroup'
        elif url.find('dashboard') >= 0:
            return 'home', None
        elif url.startswith(self.lens_home.absolute_url()) \
             or url.find('lens_edit') >= 0:  #template check for creation
            # Highlight by type: lenses
            return 'bytype', 'lens'
        elif rhaptos_obj and not self.context.portal_factory.isTemporary(rhaptos_obj):
            # on some (concrete) editor object
            return 'editobj', None
        else:
            ppath = self.context.getPhysicalPath()
            home = self.user_home
            homepath = home and home.getPhysicalPath() or None
            if homepath and ppath[:len(homepath)] == homepath:
                # Highlight by location: workspace
                return 'bylocationpersonal', None
            gwpath = self.context.portal_url.workgroups.getPhysicalPath()
            if ppath[:len(gwpath)] == gwpath:
                # Highlight by location: workgroup
                return 'bylocationgroup', None

        return None, None 


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IWorkspacePortlet)
    label = _(u"Add Rhaptos Workspace Portlet")
    description = _(u"A Rhaptos portlet that gives the user an easy way to "
                    "navigate their workspace.")

    def create(self):
        return Assignment()
