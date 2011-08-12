from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

class ProfileContent(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def content_catalog(self):
        context = aq_inner(self.context)
        return getToolByName(context,'content').catalog

    @property
    def portal_catalog(self):
        context = aq_inner(self.context)
        return getToolByName(context,'portal_catalog')

    def getAuthCollectionsForMember(self,memberid):
        query = {}
        query['portal_type'] = ['Collection',]
        query['authors'] = memberid
        query['sort_on'] = 'modified'
        query['sort_order'] = 'reverse'
        return self.content_catalog(query)

    def getAuthLinksForMember(self,memberid):
        query = {}
        query['portal_type'] = ['MemberLink',]
        query['Creators'] = memberid
        query['sort_on'] = 'modified'
        query['sort_order'] = 'reverse'
        return self.portal_catalog(query)

    def getAuthModulesForMember(self,memberid):
        query = {}
        query['portal_type'] = ['Module',]
        query['authors'] = memberid
        query['sort_on'] = 'modified'
        query['sort_order'] = 'reverse'
        return self.content_catalog(query)

    def getMaintainedModulesForMember(self,memberid):
        query = {}
        query['portal_type'] = ['Module',]
        query['maintainers'] = memberid
        query['sort_on'] = 'modified'
        query['sort_order'] = 'reverse'
        return self.content_catalog(query)



    def getTranslationsForMember(self,memberid):
        query = {}
        query['portal_type'] = ['Module',]
        query['sort_on'] = 'modified'
        query['sort_order'] = 'reverse'
        return self.content_catalog(query)


