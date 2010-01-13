from Products.CMFCore.utils import getToolByName

SKIN_LAYERS=[
'custom',
'CNXBeta',
'CNXPloneSite',
'cnx_overrides',
'CNXContent',
'rhaptos_site',
'rhaptos_overrides',
'rhaptos_content',
'rhaptos_patch',
'CNXMLFile',
'rhaptos_module_editor',
'rhaptos_workgroup',
'FeatureArticle',
'rhaptos_collection',
'ChangeSet',
'rhaptos_repository',
'rhaptos_hitcount',
'PasswordReset',
'archetypes',
'gruf',
'plone_ecmascript',
'plone_wysiwyg',
'plone_3rdParty/CMFTopic',
'plone_templates',
'plone_styles',
'plone_scripts',
'plone_portlets',
'plone_form_scripts',
'plone_prefs',
'plone_forms',
'plone_images',
'plone_content',
'cmf_legacy',
]

def _syncMetaTypes(object):
    """Fix meta_types in ObjectManager _objects to reflect actual object meta_type"""
    children = list(object._objects)
    for d in children:
        d['meta_type'] = getattr(object, d['id']).meta_type
    object._objects = tuple(children)
    
def _fixCourseMetaTypes(self):
    """Fixup course-module metatypes"""
    cat = getToolByName(self, 'portal_catalog')

    for r in cat(portal_type='Collection'):
        course = r.getObject()
        map(_syncMetaTypes, course.containedModules())

def renameMetaTypes(self):
    """Fixup meta-types that were renamed in the move to rhaptos"""
    portal = getToolByName(self, 'portal_url').getPortalObject()
    _syncMetaTypes(portal)

    map(_syncMetaTypes, portal.Members.objectValues())
    map(_syncMetaTypes, portal.GroupWorkspaces.objectValues())
    _fixCourseMetaTypes(portal)

def renameSkins(self):
    """Update the skins folders renamed in the move to rhaptos"""
    
    stool = getToolByName(self, 'portal_skins')
    stool.manage_delObjects(['RisaWorkgroup', 'ordered_plone_folder', 'risacollection',  'RisaHitCountTool', 'RisaPatch', 'RisaContent', 'RisaOverrides', 'RisaSite', 'RisaRepository', 'RisaModuleEditor'])

    stool.manage_addProduct['CMFCore'].manage_addDirectoryView('RhaptosCollection/skins/rhaptos_collection')
    stool.manage_addProduct['CMFCore'].manage_addDirectoryView('RhaptosContent/skins/rhaptos_content')
    stool.manage_addProduct['CMFCore'].manage_addDirectoryView('RhaptosHitCountTool/skins/rhaptos_hitcount')
    stool.manage_addProduct['CMFCore'].manage_addDirectoryView('RhaptosModuleEditor/skins/rhaptos_module_editor')
    stool.manage_addProduct['CMFCore'].manage_addDirectoryView('RhaptosPatchTool/skins/rhaptos_patch')
    stool.manage_addProduct['CMFCore'].manage_addDirectoryView('RhaptosRepository/skins/rhaptos_repository')
    stool.manage_addProduct['CMFCore'].manage_addDirectoryView('RhaptosSite/skins/rhaptos_overrides')
    stool.manage_addProduct['CMFCore'].manage_addDirectoryView('RhaptosSite/skins/rhaptos_site')
    stool.manage_addProduct['CMFCore'].manage_addDirectoryView('RhaptosWorkgroup/skins/rhaptos_workgroup')
    stool.selections['Connexions'] = ','.join(SKIN_LAYERS)
    stool.default_skin = 'Connexions'
    stool._p_changed = 1

def updateNavTreeProperties(self):
    """Update various navtree properties that depend on meta_type"""
    navtree = getToolByName(self, 'portal_properties').navtree_properties

    mt = list(navtree.metaTypesNotToList)
    try:
        mt.remove('RISA Module Editor')
        mt.remove('RISA Workgroup')
    except ValueError:
        pass
    mt.append('Module Editor')
    mt.append('Workgroup')        
    navtree._updateProperty('metaTypesNotToList', tuple(mt))

    mt = list(navtree.parentMetaTypesNotToQuery)
    try:
        mt.remove('')
        mt.remove('RISA Repository')
        mt.remove('RISA Repository')
    except ValueError:
        pass
    mt.append('Repository')
    navtree._updateProperty('parentMetaTypesNotToQuery', tuple(mt))

def updatePortalTypes(self):
    """Update the types tool with info that changed in the move to rhaptos"""

    ttool = getToolByName(self, 'portal_types')

    ttool.Module.manage_changeProperties(content_meta_type='Module Editor',
                                         product='RhaptosModuleEditor',
                                         factory='addModuleEditor')
                                  
    ttool.Collection.manage_changeProperties(product='RhaptosCollection')
    ttool.ContentPointer.manage_changeProperties(product='RhaptosCollection')
    ttool.PublishedContentPointer.manage_changeProperties(product='RhaptosCollection')
    ttool.SubCollection.manage_changeProperties(product='RhaptosCollection')

    ttool.Repository.manage_changeProperties(content_meta_type='Repository',
                                             product='RhaptosRepository',
                                             factory='manage_addRepository')

    ttool.Workgroup.manage_changeProperties(content_meta_type='Workgroup',
                                            product='RhaptosWorkgroup',
                                            factory='manage_addWorkgroup')
    
def addMemberProfileFields(self):
    """Customize the memberdata tool with the fields required for author profiles"""
    MEMBERDATA_PROPERTIES = (
        ('location', 'string', ''),
        ('affiliation', 'string', ''),
        ('affiliation_url','string',''),
        ('interests', 'lines', []),
        ('biography', 'lines', []),
        ('preferred_language', 'string', ''),
        ('alternative_languages','lines',[]),
        ('location','string',''),
        ('recommended_content', 'lines', []),
        )

    mdtool = getToolByName(self,'portal_memberdata')
    if mdtool.hasProperty('interests'):
        mdtool._delProperty('interests')
    for prop, tp, val in MEMBERDATA_PROPERTIES:
        if not mdtool.hasProperty(prop):
            mdtool._setProperty(prop, val, tp)
            
def renameInQuickInstaller(self):
    qi = getToolByName(self, 'portal_quickinstaller')
    contents = qi.objectItems()
    for name, obj in contents:
        if name.startswith("Risa"):
            qi.manage_delObjects(name)
            newname = "Rhaptos" + name[4:]
            try:
                obj._setId(newname)
            except AttributeError:
                # Missing Products are OK
                pass
            qi._setObject(newname, obj)

def installTransforms(self):
    qi = getToolByName(self, 'portal_quickinstaller')
    qi.installProduct('CNXMLTransforms')
    qi.uninstallProducts(['RhaptosOOoImportTool'])

def changeObjectDescriptions(self):
    tt = getToolByName(self, 'portal_types')
    tt['CNXML Document'].description = 'A CNXML Document is a text file formatted in Connexions Markup Language.' 
    tt.Module.description = 'A module is a collection of files and images about a specific topic or one aspect of a complex topic.'
    tt.File.description = 'A file is any information such as a program, text, or sound that you want to include in a module.'
    tt.Collection.description = 'A course is a grouping of related modules.'
    tt.Image.description = 'An image is a picture, drawing, or graphic to be included in a module.'

def removeMyContentConfiglet(self):
    cp = getToolByName(self, 'portal_controlpanel')
    g = list(cp.groups)
    g.remove('member|Content|Content')
    cp._updateProperty('groups',g)
    cp.unregisterConfiglet('content')

def addAccountTypeShortname(self):
    """Customize the memberdata tool with the account_type field"""

    mdtool = getToolByName(self,'portal_memberdata')
    MEMBERDATA_PROPERTIES = (('account_type', 'person', 'string'),
		             ('shortname', '', 'string'))
    for prop, val, tp in MEMBERDATA_PROPERTIES:
        if not mdtool.hasProperty(prop):
            mdtool._setProperty(prop, val, tp)
    
    cat=getToolByName(self,'member_catalog')
    indexes = cat.indexes()
    if 'status' not in indexes:
        cat.addIndex('status','KeywordIndex')
        cat.reindexIndex('status', None)
    if 'account_type' not in indexes:
        cat.addIndex('account_type','KeywordIndex')
        cat.reindexIndex('account_type',None)
