"""
Rhaptos setup functions for customizing Plone

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU General
Public License Version 2 (GPL).  See LICENSE.txt for details.
"""

## FIXME!!! not idempotent; should be made so

import os
from zLOG import INFO, ERROR
from Acquisition import aq_base
from Globals import package_home

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression
from Products.CMFCore.DirectoryView import addDirectoryViews

from Products.RhaptosSite import product_globals

def installProducts(self, portal):
    """Add any necessary portal tools"""
    qi = getToolByName(portal, 'portal_quickinstaller')
    portal_setup = getToolByName(portal, 'portal_setup')
    import_context = portal_setup.getImportContextID()
    qi.installProduct('Archetypes')
    portal_setup.setImportContext(
            'profile-Products.CMFDiffTool:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.FSImportTool:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.LinkMapTool:default')
    portal_setup.runAllImportSteps()

    qi.installProduct('PasswordResetTool')
    qi.installProduct('PloneLanguageTool')
    qi.installProduct('MasterSelectWidget')
    portal_setup.setImportContext(
            'profile-Products.UniFile:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.CNXMLDocument:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.CNXMLTransforms:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.RhaptosPatchTool:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.RhaptosWorkgroup:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.RhaptosCollection:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.RhaptosRepository:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.RhaptosHitCountTool:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.RhaptosModuleEditor:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.RhaptosModuleStorage:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.RhaptosPDFLatexTool:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.RhaptosSimilarityTool:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.RhaptosContent:default')
    portal_setup.runAllImportSteps()

    #qi.installProduct('RhaptosSite')
    portal_setup.setImportContext(
            'profile-Products.Lensmaker:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.RhaptosPrint:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.RhaptosBugTrackingTool:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.CatalogMemberDataTool:default')
    portal_setup.runAllImportSteps()
    portal_setup.setImportContext(
            'profile-Products.MathEditor:default')
    portal_setup.runAllImportSteps()

    # siyavula products...
    #portal_setup.setImportContext(
    #        'profile-Products.XMLTemplateMaker:default')
    #portal_setup.runAllImportSteps()
    #portal_setup.setImportContext(
    #        'profile-Products.LensOrganizer:default')
    #portal_setup.runAllImportSteps()
    #portal_setup.setImportContext(
    #        'profile-Products.RhaptosForums:default')
    #portal_setup.runAllImportSteps()

    portal_setup.setImportContext(import_context)


def customizeTools(self, portal):

    # FIXME: these should be in products of their own and done via an Install
    portal.manage_addProduct['RhaptosCollaborationTool'].manage_addTool('Collaboration Tool', None)

    portal.portal_patch.manage_changeProperties(title='Suggested Edits')

    # Don't import text files as Page but as File since that's what modules expect
    registry = portal.content_type_registry
    registry.assignTypeName('text', 'File')

        
def customizeMemberdata(self, portal):
    from DateTime import DateTime

    MEMBERDATA_PROPERTIES = (
        ('honorific', 'string', ''),
        ('firstname', 'string', ''),
        ('othername', 'string', ''),
        ('surname', 'string', ''),
        ('lineage', 'string', ''),
        ('homepage', 'string', ''),
        ('status', 'string', ''),
        ('comment', 'string', ''),
        ('approved_time', 'date', DateTime('2000/01/01')),
        ('location', 'string', ''),
        ('affiliation', 'string', ''),
        ('affiliation_url','string',''),
        ('interests', 'lines', []),
        ('biography', 'lines', []),
        ('preferred_language', 'string', ''),
        ('alternative_languages','lines',[]),
        ('location','string',''),
        ('recommended_content', 'lines', []),
        ('account_type', 'string', 'person'),
        ('fullname', 'string', ''),
        ('shortname', 'string', ''),
        ('visible_ids', 'boolean', 0),
        ('wysiwyg_editor', 'string', 'Kupu'),
        )

    mdtool = getToolByName(portal,'portal_memberdata')
    if mdtool.hasProperty('interests'):
        mdtool._delProperty('interests')
    for prop, tp, val in MEMBERDATA_PROPERTIES:
        if not mdtool.hasProperty(prop):
            mdtool._setProperty(prop, val, tp)
            
    mdtool._updateProperty('listed', 1)
    mdtool._updateProperty('visible_ids', 0)        


def customizeMemberCatalog(self, portal):

    from Products.ManagableIndex.FieldIndex import FieldIndex

    # Customize the member_catalog indexes
    catalog = getToolByName(portal, 'member_catalog')
    catalog.addIndex('firstname', 'FieldIndex')
    catalog.addIndex('approved_time', 'DateIndex')
    catalog.addColumn('approved_time')

    # Replace email index with Managable FieldIndex
    catalog.delIndex('email')
    index = FieldIndex('email')
    catalog._catalog.addIndex('email', index)
    index._updateProperty('TermType', 'string')

    # New Managable FieldIndex for surname so we can sort on it
    index = FieldIndex('surname')
    catalog._catalog.addIndex('surname', index)
    index._updateProperty('TermType', 'string')
    index._updateProperty('PrenormalizeTerm', 'python: value.lower()')

    

def customizeMembershipTool(self, portal):

    mt = getToolByName(portal, 'portal_membership')

    mt.setMemberAreaType('Workspace')


    
def customizeActions(self, portal):
    pa_tool=getToolByName(portal,'portal_actions')

    actions=pa_tool._cloneActions()
    order = ['Content', 'Lenses', 'About Us', 'Help', 'MyCNX']
    toorder = list()
    tmp_actions = list()
    for a in actions:
        if a.id == 'index_html':
            a.title = 'Home'
        elif a.id == 'delete':
            a.title = 'Remove'
        elif a.id in ('Members', 'news', 'search_form', 'change_status', 'small_text', 'normal_text', 'large_text', 'sendto', 'print', 'change_state', 'addtofavorites'):
            a.visible = 0
        if a.title in order:
            a.visible = 1
            toorder.append((order.index(a.title), a))
        else:
            tmp_actions.append(a)
    actions = tmp_actions
    toorder.sort()
    for i,a in toorder:
        actions.append(a)
    pa_tool._actions=tuple(actions)


    #pa_tool.addAction('courses', 'Courses', 'string:$portal_url/content/browse_course_titles','', 'View', 'site_actions')

    m_tool=getToolByName(portal,'portal_membership')
    for a in m_tool._actions:
        if a.id == 'mystuff':
            a.title = 'My Workspace'
            a.action = Expression('string:${portal/portal_membership/getHomeUrl}/workspace_contents')
        elif a.id == 'preferences':
            a.title = 'My Account'
    m_tool._p_changed = 1

    u_tool=getToolByName(portal,'portal_undo')
    actions=u_tool._cloneActions()
    for a in actions:
        if a.id == 'undo':
            a.visible = 0
    u_tool._actions=actions


def customizeControlPanel(self, portal):
    from Products.CMFCore.CMFCorePermissions import SetOwnProperties
    groups = ['site|Plone|Plone Configuration',
              'site|Products|Add-on Product Configuration',
              'member|Member|Account Maintenance',
              'member|Collaboration|Collaboration Requests',
              ]

    configlets = (
        {'id':'Collaborations',
         'appId':'Collaborations',
         'name':'Role Requests',
         'action':'string:${portal_url}/collaborations',
         'permission': SetOwnProperties,
         'category':'Collaboration',
         },
        {'id':'Patches',
         'appId':'Patches',
         'name':'Suggested Edits',
         'action':'string:${portal_url}/patches',
         'permission': SetOwnProperties,
         'category':'Collaboration',
         },
        )
    cp_tool = getToolByName(portal, 'portal_controlpanel')
    cp_tool._updateProperty('groups', groups)
    cp_tool.registerConfiglets(configlets)

def customizeObjectDescriptions(self, portal):
    tt = getToolByName(portal, 'portal_types')
    tt['CNXML Document'].description = 'A CNXML Document is a text file formatted in Connexions Markup Language.' 
    tt.Module.description = 'A module is a collection of files and images about a specific topic or one aspect of a complex topic.'
    tt.File.description = 'A file is any information such as a program, text, or sound that you want to include in a module.'
    tt.Collection.description = 'A course is a grouping of related modules.'
    tt.Image.description = 'An image is a picture, drawing, or graphic to be included in a module.'
    
def customizeSlots(self, portal):
    left_slots=[
                'here/portlet_navigation/macros/portlet',
                'here/workspaces_slot/macros/portlet',
                ]

    right_slots=[
                 'here/portlet_loggedin/macros/portlet',
                 'here/portlet_login/macros/portlet',
                 'here/portlet_news/macros/portlet',
                 'here/portlet_review/macros/portlet',
                 ]

    portal.manage_changeProperties(left_slots=left_slots,
                                   right_slots=right_slots)

    # WS Slots
    right_slots = ['here/log_action_slot/macros/portlet']

    portal.Members._updateProperty('right_slots', right_slots)
    wsfolder = portal.portal_groups.getGroupWorkspacesFolder()
    if wsfolder.hasProperty('right_slots'):
        wsfolder._updateProperty('right_slots', right_slots)
    else:
        wsfolder._setProperty('right_slots', right_slots, type='lines')


def customizeSkins(self, portal):
    st = getToolByName(portal, 'portal_skins')

    # We need to add Filesystem Directory Views for any directories in
    # our skins/ directory.  These directories should already be
    # configured.
    addDirectoryViews(st, 'skins', product_globals)

    # FIXME: we need a better way of constructing this
    pathlist= [p.strip() for p in st.getSkinPath('Plone Default').split(',')]
    pathlist.insert(1, 'rhaptos_site')
    pathlist.insert(1, 'rhaptos_overrides')
    path = ','.join(pathlist)

    # Create a new 'Rhaptos' skin
    st.addSkinSelection('Rhaptos', path, make_default=1)

    # disallow changing of skins (skin flexibility)
    st.allow_any = 0

def customizeTypes(self, portal):
    types_tool=getToolByName(portal,'portal_types')

    actions=types_tool.ChangeSet._cloneActions()
    for a in actions:
        if a.id == 'edit':
            a.visible = 0
    types_tool.ChangeSet._actions=actions

    # Customize Workgroup type
    # XXX this breaks the workspace_contents template which expects
    # allowed_content_types to be set to ('Collection', 'Module',
    # "UnifiedFile')
    #wg = getattr(types_tool, 'Workgroup')
    #wg.manage_changeProperties(immediate_view='folder_contents',
    #                           filter_content_types=1,
    #                           allowed_content_types=('File', 'Image', 'Module', 'Collection'))

def customizeWorkflow(self, portal):
    wf_tool=getToolByName(portal,'portal_workflow')
    wf_tool.setChainForPortalTypes(['Workspace'],'')
    wf_tool.setChainForPortalTypes(['Image'],'')
    wf_tool.setChainForPortalTypes(['File'],'')
    wf_tool.setChainForPortalTypes(['ChangeSet'],'')
    wf_tool.setChainForPortalTypes(['Large Plone Folder'],'')
    wf_tool.setChainForPortalTypes(['Collection','SubCollection', 'ContentPointer', 'PublishedContentPointer'],'')


def customizePermissions(self, portal):
    portal._addRole('Author')
    portal._addRole('Maintainer')
    portal._addRole('Licensor')        

    # FIXME: we'd prefer not to give Anonymous users 'Add'
    # permission here, but currently new member folders get
    # created upon joining, at which point the user is still
    # anonymous.  There ought to be a better way...
    portal.Members.manage_permission('Add portal content', ('Anonymous', 'Member',), acquire=1)
    portal.Members.manage_permission('Add Annotation Servers', ('Manager', 'Owner',), acquire=1)
    portal.Members.manage_permission('Delete objects', ('Maintainer', 'Owner',), acquire=1)
    portal.Members.manage_permission('Change Images and Files', ('Maintainer', 'Owner',), acquire=1)
    portal.Members.manage_permission('List folder contents', ('Manager', 'Owner',), acquire=0)
    portal.Members.manage_permission('Use external editor', ('Maintainer', 'Owner',), acquire=1)        
    portal.Members.manage_permission('View', ('Manager', 'Owner',), acquire=0)

    groups = portal.portal_groups.getGroupWorkspacesFolder()
    groups.manage_permission('Add Annotation Servers', ('Manager', 'Owner',), acquire=1)
    groups.manage_permission('Add portal content', ('Member',), acquire=1)
    groups.manage_permission('Delete objects', ('Maintainer', 'Owner',), acquire=1)
    groups.manage_permission('Change Images and Files', ('Maintainer', 'Owner',), acquire=1)
    groups.manage_permission('List folder contents', ('Manager', 'Owner',), acquire=0)
    groups.manage_permission('Use external editor', ('Maintainer', 'Owner',), acquire=1)
    groups.manage_permission('View', ('Manager', 'Owner',), acquire=0)

    portal.content.manage_permission('Add portal content', ('Member',), acquire=1)

    portal.manage_permission('Add Groups', ('Member',), acquire=1)
    #portal.manage_permission('Add Annotation Servers', ('Owner',), acquire=1)
    portal.manage_permission('Manage Groups', ('Owner',), acquire=1)
    portal.manage_permission('Manage WebDAV Locks', ('Owner',), acquire=1)
    portal.manage_permission('View Groups', ('Member',), acquire=1)
    portal.manage_permission('Edit Rhaptos Object', ('Maintainer',), acquire=1)

    # FIXME: we really don't want to do this, but must so that nextID gets updated
    groups.manage_permission('Manage properties', ('Member',), acquire=1)        

def customizeNavTree(self, portal):
    navtree = getToolByName(portal, 'portal_properties').navtree_properties
#    navtree._updateProperty('rolesSeeContentsView', ['Manager', 'Reviewer'])
    mt = list(navtree.metaTypesNotToList)
    mt.append('Module Editor')
    mt.append('Workgroup')        
    mt.append('News Item')
    mt.append('Portal File')
    mt.append('Portal Image')
    mt.append('Change Set')        
    navtree._updateProperty('metaTypesNotToList', tuple(mt))

def customizeWorkspaceFolders(self, portal):
    gt = getToolByName(portal, 'portal_groups')
    tt = getToolByName(portal, 'portal_types')
    gt.setGroupWorkspaceContainerType('Large Plone Folder')

    groups = gt.getGroupWorkspacesFolder()
    if groups is None:
        # Can't use invokeFactory here because Large Plone Folder isn't allowed; constructContent bypasses permissions
        tt.constructContent(gt.getGroupWorkspaceContainerType(), portal, gt.getGroupWorkspacesFolderId())
        groups = gt.getGroupWorkspacesFolder()

    groups._updateProperty('title', 'Workgroups')
    groups._setProperty('nextID', 0, type='int')

def customizePortal(self, portal):
    props_tool=getToolByName(portal,'portal_properties')
    props_tool.site_properties._updateProperty('ext_editor', 1)
    portal._updateProperty('validate_email',1)

    # Work around bug in PloneTool.browserDefault() where skins
    # don't get searched for default pages unless they're
    # explictly set as a property
#    portal._setProperty('default_page', 'index_html')

#def customizePortalCatalog(self, portal):
#    cat_tool=getToolByName(portal,'portal_catalog')
#    cat_tool.addIndex('getObjPositionInParent', 'FieldIndex')

def customizeFrontPage(self, portal):
    # FIXME: currently disabled until we have better text to go here
    try:
        portal.manage_delObjects('index_html')
    except AttributeError:
        pass
    portal.invokeFactory('Document', 'index_html')
    frontpage = portal.index_html
    frontpage.title = 'Welcome to Rhaptos'
    path = os.path.join(package_home(product_globals), 'www/index_html')
    f = open(path)
    content = f.read()
    f.close()
    frontpage.edit('html',content)


def customizeHelpContent(self, portal):
    portal.invokeFactory('Folder', 'help')
    portal.help.invokeFactory('Folder', 'reference')
    files = ['roles', 'status', 'workgroups']
    for name in files:
        portal.help.reference.invokeFactory('Document', name)
        path = os.path.join(package_home(product_globals), 'www/help/reference', name)
        f = open(path)
        content = f.read()
        f.close()
        doc = getattr(portal.help.reference, name)
        doc.edit('structured-text', content)
        doc.title = name.capitalize()

def customizeFactoryTool(self, portal):
    f_tool = getToolByName(portal, 'portal_factory')
    f_tool.manage_setPortalFactoryTypes(listOfTypeIds=['Collection', 'Module', 'Image', 'File'])


def customizeDiffTool(self, portal):
    d_tool = getToolByName(portal, 'portal_diff')
    
    d_tool.setDiffField('CNXML Document', 'data', 'Lines Diff')
    d_tool.setDiffField('File', 'data', 'Binary Diff')
    d_tool.setDiffField('Image', 'data', 'Binary Diff')
    d_tool.setDiffField('Module', 'abstract', 'Field Diff')
    d_tool.setDiffField('Module', 'authors', 'List Diff')
    d_tool.setDiffField('Module', 'licensors', 'List Diff')
    d_tool.setDiffField('Module', '_links', 'Links Diff')
    d_tool.setDiffField('Module', 'keywords', 'List Diff')
    d_tool.setDiffField('Module', 'maintainers', 'List Diff')
    d_tool.setDiffField('Module', 'title', 'Field Diff')

def setPASPlugins(self, portal):
    
    pas = getToolByName(portal,'acl_users')
    found = getattr(pas, 'xuf_hash', None)
    if not found:
        pas.manage_addProduct['RhaptosSite'].addAltHashAuth('xuf_hash')
        plugin = pas['xuf_hash']
        plugin.manage_activateInterfaces(['IAuthenticationPlugin'])

def createHelpSection(self, portal):
    if 'help' not in portal.objectIds():
        portal._importObjectFromFile(
            os.path.join(os.path.dirname(__file__), 'data', 'help.zexp'),
            verify=False,
            set_owner=True)

def createCollectionPrinter(self, portal):
    if 'RCPrinter' not in portal.objectIds():
        portal.manage_addProduct['RhaptosCollection'].manage_addAsyncPrinter(
                'RCPrinter', '', '', '', '')

def creataAboutUSSection(self, portal):
    if 'aboutus' not in portal.objectIds():
        portal.invokeFactory('Folder', 'aboutus')
        folder = portal.aboutus
        folder.setTitle('About')
        folder.invokeFactory('Document', 'placeholder')
        placeholder = folder.placeholder
        placeholder.setTitle('Placeholder')
        text = ('<p>This is a placeholder for the default about us page. '
                'To replace it create a new Document and use the display '
                'dropdown on the aboutus folder to change the default view.'
                '</p>')
        placeholder.edit('html', text)
        folder.setDefaultPage('placeholder')

def addPDFsFolder(self, portal):
    portal_types = getToolByName(portal, 'portal_types')
    large_folder = portal_types['Large Plone Folder']
    large_folder.manage_changeProperties(global_allow=True)
    if 'pdfs' not in portal.objectIds():
        portal.invokeFactory('Large Plone Folder', 'pdfs')
    large_folder.manage_changeProperties(global_allow=False)

functions = {
    'Install Products': installProducts,
    'Customize Tools': customizeTools,
    'Customize Member Data': customizeMemberdata,
    'Customize Membership Tool': customizeMembershipTool,
    'Customize Workspaces': customizeWorkspaceFolders,
    'Customize Actions': customizeActions,
    'Customize Portlets': customizeSlots,
    'Customize Skins': customizeSkins,
    'Customize Types': customizeTypes,
    'Customize Workflow': customizeWorkflow,
    'Customize Permissions': customizePermissions,
    'Customize NavTree': customizeNavTree,
    'Customize Portal': customizePortal,
#    'Customize Portal Catalog': customizePortalCatalog,
    'Customize Front Page': customizeFrontPage,
    'Customize Member Catalog':customizeMemberCatalog,
    'Customize Control Panel':customizeControlPanel,
    'Customize Factory Tool':customizeFactoryTool,
    'Customize Diff Tool':customizeDiffTool,
    'Customize Object Descriptions':customizeObjectDescriptions,
    'Set PAS Plugins':setPASPlugins,
    'Create Help Section': createHelpSection,
    'Create Collection Printer': createCollectionPrinter,
    'Create About Us Section': creataAboutUSSection,
    'Create PDFs Folder': addPDFsFolder,
    }

class RhaptosSetup:
    type = 'Rhaptos Setup'

    description = "Site customizations for <a href='http://software.cnx.rice.edu/'>Rhaptos</a>"

    functions = functions

    ## This line and below may not be necessary at some point
    ## in the future. A future version of Plone may provide a
    ## superclass for a basic SetupWidget that will safely
    ## obviate the need for these methods.
     
    single = 0
  
    def __init__(self, portal):
        self.portal = portal
  
    def setup(self):
        pass
 
    def delItems(self, fns):
        out = []
        out.append(('Currently there is no way to remove a function', INFO))
        return out
 
    def addItems(self, fns):
        out = []
        for fn in fns:
            self.functions[fn](self, self.portal)
            out.append(('Function %s has been applied' % fn, INFO))
        return out
 
    def active(self):
        return 1
                                                                                 
    def installed(self):
        return []
 
    def available(self):
        """ Go get the functions """
        # We return an explicit list here instead of just functions.keys() since order matters
        return [
            'Install Products',
            'Customize Tools',
            'Customize Member Data',
            'Customize Member Catalog',
            'Customize Membership Tool',
            'Customize Workspaces',
            'Customize Actions',
            'Customize Portlets',
            'Customize Skins',
            'Customize Types',
            'Customize Workflow',
            'Customize Permissions',
            'Customize NavTree',
            'Customize Portal',
#            'Customize Portal Catalog',
            'Customize Front Page',
            'Customize Control Panel',
            'Customize Diff Tool',
            'Customize Object Descriptions',
            'Set PAS Plugins',
            'Create Help Section',
            'Create Collection Printer',
            'Create About Us Section',
            'Create PDFs Folder',
            ]
