# -*- coding: utf-8 -*-
from zope.component.hooks import getSite
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces import IPloneSiteRoot


class SiteLicenseView(BrowserView):
    """Render the site license from any location in the site."""

    index = ViewPageTemplateFile('templates/site-license.pt')

    def __call__(self):
        if not IPloneSiteRoot.providedBy(self.context):
            # Ensure we are at root of the site to get the correct set
            # of portlets.
            site = getSite()
            site_path = site.getPhysicalPath()
            path = self.request.physicalPathToURL(site_path)
            self.request.response.redirect("%s/@@site-license" % path)
        return self.index()

    # TODO: Add a lookup for the site-license content item, redirection,
    #       or page template.
