#
# RhaptosTestCase
#
from Testing import ZopeTestCase
import transaction

ZopeTestCase.installProduct('CMFCore')
ZopeTestCase.installProduct('CMFDefault')
ZopeTestCase.installProduct('CMFCalendar')
ZopeTestCase.installProduct('CMFTopic')
ZopeTestCase.installProduct('DCWorkflow')
ZopeTestCase.installProduct('CMFActionIcons')
ZopeTestCase.installProduct('CMFQuickInstallerTool')
ZopeTestCase.installProduct('CMFFormController')
ZopeTestCase.installProduct('GroupUserFolder')
ZopeTestCase.installProduct('ZCTextIndex')
ZopeTestCase.installProduct('CMFPlone')
ZopeTestCase.installProduct('MailHost', quiet=1)
ZopeTestCase.installProduct('PageTemplates', quiet=1)
ZopeTestCase.installProduct('PythonScripts', quiet=1)
ZopeTestCase.installProduct('ExternalMethod', quiet=1)
ZopeTestCase.installProduct('RhaptosSite')
ZopeTestCase.installProduct('Archetypes')
ZopeTestCase.installProduct('MimetypesRegistry')
ZopeTestCase.installProduct('PortalTransforms')
ZopeTestCase.installProduct('CNXMLDocument')
ZopeTestCase.installProduct('CVSTool')
ZopeTestCase.installProduct('FSImportTool')
ZopeTestCase.installProduct('ZCatalog')
ZopeTestCase.installProduct('ZPsycopgDA')
ZopeTestCase.installProduct('ZSQLMethods')
ZopeTestCase.installProduct('CatalogMemberDataTool')
ZopeTestCase.installProduct('CMFDiffTool')
ZopeTestCase.installProduct('LinkMapTool')
ZopeTestCase.installProduct('PloneLanguageTool')
ZopeTestCase.installProduct('PasswordResetTool')
ZopeTestCase.installProduct('RhaptosPatchTool')
ZopeTestCase.installProduct('RhaptosCollection')
ZopeTestCase.installProduct('RhaptosRepository')
ZopeTestCase.installProduct('RhaptosHitCountTool')
ZopeTestCase.installProduct('RhaptosModuleStorage')
ZopeTestCase.installProduct('RhaptosPDFLatexTool')
ZopeTestCase.installProduct('RhaptosSimilarityTool')
ZopeTestCase.installProduct('RhaptosCollaborationTool')

import PloneTestCase

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base
import time
import types
import DateTime

portal_name = 'portal'
portal_owner = 'portal_owner'
default_user = ZopeTestCase.user_name

class RhaptosTestCase(PloneTestCase.PloneTestCase):
    '''TestCase for Rhaptos testing'''
    
    def beforeTearDown(self):
        """Remove the testrepository"""
        pass
        

def setupRhaptosSite(app=None, id=portal_name, quiet=0, with_default_memberarea=1):
    '''Creates a Rhaptos site.'''
    if not hasattr(aq_base(app), id):
        _start = time.time()
        if not quiet: ZopeTestCase._print('Adding Rhaptos Site ... ')
        # Add user and log in
        app.acl_users._doAddUser(portal_owner, '', ['Manager'], [])
        user = app.acl_users.getUserById(portal_owner).__of__(app.acl_users)
        newSecurityManager(None, user)
        # Add Rhaptos Site
        factory = app.manage_addProduct['RhaptosSite']
        u_str = str(DateTime.DateTime()).replace(' ','').replace('.','').replace(':','').replace('/','').replace('-','').lower()
        factory.manage_addRhaptosSite(id, '', create_userfolder=1, dbauser='postgres', dbuser='testuser', dbname='testrepository' + u_str)
        # Precreate default memberarea for performance reasons
        if with_default_memberarea:
            PloneTestCase._setupHomeFolder(app[id], default_user)
        # Log out
        noSecurityManager()
        transaction.commit()
        if not quiet: ZopeTestCase._print('done (%.3fs)\n' % (time.time()-_start,))

# Create a Plone site in the test (demo-) storage
#app = ZopeTestCase.app()
#setupRhaptosSite(app)
#ZopeTestCase.close(app)
