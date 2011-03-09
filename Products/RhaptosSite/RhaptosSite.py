# -*- coding: utf-8 -*-
from Products.CMFPlone.factory import addPloneSite
from Products.PageTemplates.PageTemplateFile import PageTemplateFile


__version__='1.1'


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

    site = addPloneSite(self, id, title, description, create_userfolder,
                        email_from_address, email_from_name, validate_email,
                        extension_ids=('Products.RhaptosSite:default',))

    RESPONSE.redirect('%s/manage_main' % site.absolute_url())


def register(context, globals):
    context.registerClass(meta_type='Rhaptos Site',
                          permission='Add CMF Sites',
                          constructors=(manage_addSiteForm,
                                        manage_addRhaptosSite,) )
