import os, sys, re

from zope.interface import implements

import Globals
from ComputedAttribute import ComputedAttribute
from Products.CMFPlone import cmfplone_globals
from Products.CMFDefault.Portal import CMFSite
from Products.CMFPlone.Portal import PloneSite
from Products.CMFCore import permissions
from Products.CMFCore.TypesTool import FactoryTypeInformation
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault import Portal, DublinCore
from Products.CMFPlone.PloneFolder import OrderedContainer
#from Products.CMFPlone.Portal import manage_addSite   # jcc TODO breaks install!
from Products.CMFPlone.factory import addPloneSite
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from AccessControl import ClassSecurityInfo

__version__='1.1'

class RhaptosSite(PloneSite, CMFSite, OrderedContainer):
    """
    RhaptosSite is a PloneSite which uses the Rhaptos Site
    customization policy and database
    """
    security=ClassSecurityInfo()
    meta_type = portal_type = 'Rhaptos Site'

Globals.InitializeClass(RhaptosSite)

manage_addSiteForm = PageTemplateFile('www/addRhaptosSite', globals())
manage_addSiteForm.__name__ = 'addRhaptosSite'
def manage_addRhaptosSite(self, id, title='', description='',
                          create_userfolder=1,
                          email_from_address='',
                          email_from_name='Rhaptos',
                          validate_email=0,
                          dbauser='rhaptos_dba',
                          dbapass=None,
                          dbuser='rhaptos',
                          dbpass=None,
                          dbname='repository',
                          dbserver=None,
                          dbport=None,
                          RESPONSE=None):
    """ Rhaptos Site factory """
    temp_id = 'DB_OPTS_TEMP'
    if not hasattr(self.aq_parent.aq_parent,temp_id):
        self.aq_parent.aq_parent.manage_addFolder(temp_id)
    root = self.aq_parent.aq_parent[temp_id]
    root._dbopts={}
    root._dbopts['admin']=dbauser
    root._dbopts['adminpass']=dbapass
    root._dbopts['user']=dbuser
    root._dbopts['userpass']=dbpass
    root._dbopts['dbname']=dbname
    root._dbopts['server']=dbserver
    root._dbopts['port']=dbport

    #manage_addSite(self, id, title, description, create_userfolder, email_from_address, email_from_name, validate_email, custom_policy='Rhaptos Site', RESPONSE=RESPONSE)
    addPloneSite(self, id, title, description, create_userfolder, email_from_address, email_from_name, validate_email, RESPONSE=RESPONSE, extension_ids=('RhaptosSite:rhaptos-default',))

    
def register(context, globals):
    context.registerClass(meta_type='Rhaptos Site',
                          permission='Add CMF Sites',
                          constructors=(manage_addSiteForm,
                                        manage_addRhaptosSite,) )

class RhaptosGenerator():

    def create(self, parent, id, create_userfolder):
        plone = PloneGenerator().create(parent, id, create_userfolder)

        #Attach DB parameters to the portal
        plone._dbopts=parent._dbopts
        
        return plone
