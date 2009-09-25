from __future__ import nested_scopes
from ComputedAttribute import ComputedAttribute
from Products.CMFPlone import cmfplone_globals
from Products.CMFPlone import custom_policies
from Products.CMFPlone import ToolNames
from Products.CMFDefault.Portal import CMFSite
from Products.CMFPlone.Portal import PloneSite
from Products.CMFPlone.setuphandlers import PloneGenerator
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.TypesTool import FactoryTypeInformation
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault import Portal, DublinCore
from Products.CMFPlone.PloneFolder import OrderedContainer
from Products.CMFDefault.Portal import manage_addCMFSite
#from Products.CMFPlone.Portal import manage_addSite   # jcc TODO breaks install!
from Products.CMFPlone.factory import addPloneSite
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
import Globals
import os, sys, re

from AccessControl import ClassSecurityInfo

__version__='1.1'

class RhaptosSite(PloneSite, CMFSite, OrderedContainer):
    """
    RhaptosSite is a PloneSite which uses the Rhaptos Site
    customization policy and database
    """
    security=ClassSecurityInfo()
    meta_type = portal_type = 'Rhaptos Site'
    __implements__ = DublinCore.DefaultDublinCoreImpl.__implements__ + \
                     OrderedContainer.__implements__

Globals.InitializeClass(RhaptosSite)

manage_addSiteForm = PageTemplateFile('www/addRhaptosSite', globals())
manage_addSiteForm.__name__ = 'addRhaptosSite'
def manage_addRhaptosSite(self, id, title='Portal', description='',
                          create_userfolder=1,
                          email_from_address='postmaster@localhost',
                          email_from_name='Portal Administrator',
                          validate_email=0,
                          RESPONSE=None):
    """ Rhaptos Site factory """

    #manage_addSite(self, id, title, description, create_userfolder, email_from_address, email_from_name, validate_email, custom_policy='Rhaptos Site', RESPONSE=RESPONSE)
    addPloneSite(self, id, title, description, create_userfolder, email_from_address, email_from_name, validate_email, RESPONSE=RESPONSE, extension_ids=('RhaptosSite:rhaptos-default',))

    
def register(context, globals):
    context.registerClass(meta_type='Rhaptos Site',
                          permission='Add CMF Sites',
                          constructors=(manage_addSiteForm,
                                        manage_addRhaptosSite,) )

class RhaptosGenerator(PloneGenerator):

    def create(self, parent, id, create_userfolder):
        plone = PloneGenerator().create(parent, id, create_userfolder)

        #Attach DB parameters to the portal
        plone._dbopts=parent._dbopts
        
        return plone
