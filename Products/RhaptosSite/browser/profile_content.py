from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from zope.i18n import translate
from Products.RhaptosSite import RhaptosMessageFactory as _

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

    @property
    def portal_membership(self):
        context = aq_inner(self.context)
        return getToolByName(context,'portal_membership')

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

    def getFeaturedContentForMember(self,memberid):
        query = {}
        query['portal_type'] = ['MemberFeaturedContent',]
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

    def has_maintained_content(self,memberid):
        m_mods = len(self.getMaintainedModulesForMember(memberid)) > 0
        m_colls = len(self.getMaintainedCollectionsForMember(memberid)) > 0
        return m_mods or m_colls

    def getMaintainedCollectionsForMember(self,memberid):
        query = {}
        query['portal_type'] = ['Collection',]
        query['maintainers'] = memberid
        query['sort_on'] = 'modified'
        query['sort_order'] = 'reverse'
        return self.content_catalog(query)

    def getTranslationsForMember(self,memberid):
        query = {}
        query['portal_type'] = ['Module',]
        query['sort_on'] = 'modified'
        query['translators'] = memberid
        query['sort_order'] = 'reverse'
        return self.content_catalog(query)

    def getTranslationsCollectionsForMember(self,memberid):
        query = {}
        query['portal_type'] = ['Module',]
        query['sort_on'] = 'modified'
        query['translators'] = memberid
        query['sort_order'] = 'reverse'
        return self.content_catalog(query)

    def has_translated_content(self,memberid):
        t_mods = len(self.getTranslationsForMember(memberid)) > 0
        t_colls = len(self.getTranslationsCollectionsForMember(memberid)) > 0
        return t_mods or t_colls

    def content_url(self,memberid):
        data = {}
        data['memberid'] = member = self.portal_membership.getMemberById(memberid)
        data['first_letter'] = member.surname and member.surname[0] or member.shortname and member.shortname[0]
	content_url = """/content/expanded_browse_authors?letter=%(first_letter)s&author=%(memberid)s"""
        return content_url % data


    def content_authored_statement(self,memberid):
        auth_colls = self.getAuthCollectionsForMember(memberid)
        auth_mods = self.getAuthModulesForMember(memberid)
        mod_count = len(auth_mods)
        coll_count = len(auth_colls)
        if mod_count < 1 and coll_count < 1:
            return translate(_('No items yet',
                                default = u'No items yet',
                                ))

        if mod_count > 1 and coll_count > 1: 
            return translate(_('X Modules and Y Collections',
                                default = u'${mod_count} Modules and ${coll_count} Collections',
                                mapping = {u'mod_count': mod_count,
                                           u'coll_count': coll_count}))

        if mod_count == 1 and coll_count > 1: 
            return translate(_('X Module and Y Collections',
                                default = u'${mod_count} Module and ${coll_count} Collections',
                                mapping = {u'mod_count': mod_count,
                                           u'coll_count': coll_count}))

        if mod_count == 1 and coll_count == 1: 
            return translate(_('X Module and Y Collection',
                                default = u'${mod_count} Module and ${coll_count} Collection',
                                mapping = {u'mod_count': mod_count,
                                           u'coll_count': coll_count}))

        if mod_count > 1 and coll_count == 1: 
            return translate(_('X Modules and Y Collection',
                                default = u'${mod_count} Modules and ${coll_count} Collection',
                                mapping = {u'mod_count': mod_count,
                                           u'coll_count': coll_count}))

    def content_maintained_statement(self,memberid):
        maintained_mods = self.getMaintainedModulesForMember(memberid)
        maintained_colls = self.getMaintainedCollectionsForMember(memberid)
        mod_count = len(maintained_mods)
        coll_count = len(maintained_colls)
        if mod_count < 1 and coll_count < 1:
            return translate(_('No items yet',
                                default = u'No items yet',
                                ))

        if mod_count > 1 and coll_count > 1: 
            return translate(_('X Modules and Y Collections',
                                default = u'${mod_count} Modules and ${coll_count} Collections',
                                mapping = {u'mod_count': mod_count,
                                           u'coll_count': coll_count}))

        if mod_count == 1 and coll_count > 1: 
            return translate(_('X Module and Y Collections',
                                default = u'${mod_count} Module and ${coll_count} Collections',
                                mapping = {u'mod_count': mod_count,
                                           u'coll_count': coll_count}))

        if mod_count == 1 and coll_count == 1: 
            return translate(_('X Module and Y Collection',
                                default = u'${mod_count} Module and ${coll_count} Collection',
                                mapping = {u'mod_count': mod_count,
                                           u'coll_count': coll_count}))

        if mod_count > 1 and coll_count == 1: 
            return translate(_('X Modules and Y Collection',
                                default = u'${mod_count} Modules and ${coll_count} Collection',
                                mapping = {u'mod_count': mod_count,
                                           u'coll_count': coll_count}))

    def content_translated_statement(self,memberid):
        translated_mods = self.getTranslationsForMember(memberid)
        translated_colls = self.getTranslationsCollectionsForMember(memberid)
        mod_count = len(translated_mods)
        coll_count = len(translated_colls)

        if mod_count > 1:  
            return translate(_('X Modules',
                                default = u'${mod_count} Modules',
                                mapping = {u'mod_count': mod_count,
                                           }))
        if mod_count == 1:  
            return translate(_('X Module',
                                default = u'${mod_count} Module',
                                mapping = {u'mod_count': mod_count,
                                           }))

        if mod_count < 1 and coll_count < 1:
            return translate(_('No items yet',
                                default = u'No items yet',
                                ))

        if mod_count > 1 and coll_count > 1: 
            return translate(_('X Modules and Y Collections',
                                default = u'${mod_count} Modules and ${coll_count} Collections',
                                mapping = {u'mod_count': mod_count,
                                           u'coll_count': coll_count}))

        if mod_count == 1 and coll_count > 1: 
            return translate(_('X Module and Y Collections',
                                default = u'${mod_count} Module and ${coll_count} Collections',
                                mapping = {u'mod_count': mod_count,
                                           u'coll_count': coll_count}))

        if mod_count == 1 and coll_count == 1: 
            return translate(_('X Module and Y Collection',
                                default = u'${mod_count} Module and ${coll_count} Collection',
                                mapping = {u'mod_count': mod_count,
                                           u'coll_count': coll_count}))

        if mod_count > 1 and coll_count == 1: 
            return translate(_('X Modules and Y Collection',
                                default = u'${mod_count} Modules and ${coll_count} Collection',
                                mapping = {u'mod_count': mod_count,
                                           u'coll_count': coll_count}))
