"""
monkeypatch.py - fix software that we don't really want to patch directly, using the magic of Python

Author: Brent Hendricks and J. Cameron Cooper
(C) 2005 Rice University

This software is subject to the provisions of the GNU General
Public License Version 2 (GPL).  See LICENSE.txt for details.
"""


import logging
logger = logging.getLogger('RhaptosSite')


## Monkey patch MemberData deprecation warnings out of existence, since they are too common
from Products.CMFPlone import MemberDataTool

if not hasattr(MemberDataTool, 'RhaptosSite_noMDdeprecated_patch'):
    logger.info("Patching Products.CMFPlone.MemberDataTool.log_deprecated")

    MemberDataTool.RhaptosSite_noMDdeprecated_patch = 1
    
    MemberDataTool.log_deprecated = lambda *args,**kw:None

## Monkeypatch MemberDataTool to write member properties to the database; used to be in custom tool

from Products.PlonePAS.tools.memberdata import MemberData
DB_FIELDS = ['honorific', 'firstname', 'othername', 'surname', 'fullname', 'lineage', 'email', 'homepage', 'comment']

if not hasattr(MemberData, 'RhaptosSite_setMemberProperties_patch'):
    logger.info("Patching PlonePAS.tools.memberdata.MemberData.setMemberProperties")

    MemberData.RhaptosSite_setMemberProperties_patch = 1

    from Products.PlonePAS.tools.memberdata import *     # get all the original's imports and definitions
    from ZPublisher.Converters import type_converters

    def setMemberProperties(self, mapping):
        """ Set extended properties on this member.
        Overridden to store a copy of certain user data fields in an SQL database.
        Dispatches to the method it over-rides, as well, so (generally) PAS can do what it
        needs to do.
        """
        # Only pass relevant fields to the database
        db_args = dict([(f, v) for (f, v) in mapping.items() if f in DB_FIELDS and self.getProperty(f) != v])
        dbtool = getToolByName(self, 'portal_moduledb')
        if dbtool and db_args:
            # We have to pass in aq_parent to be our own parent,
            # otheriwse the ZSQL method will acquire blank arguments
            # from the property sheet
            if not self.member_catalog(getUserName=self.getId()):
                #logger.info("INSERT memberdata for %s: %s" % (self.getId(), db_args))
                dbtool.sqlInsertMember(aq_parent=self.aq_parent, id=self.getId(), **db_args)
            else:
                #logger.info("UPDATE memberdata for %s: %s" % (self.getId(), db_args))
                dbtool.sqlUpdateMember(aq_parent=self.aq_parent, id=self.getId(), **db_args)

        # also, set property on MemberData so it can be cataloged
        tool = self.getTool()
        for id in tool.propertyIds():
            if mapping.has_key(id):
                if not self.__class__.__dict__.has_key(id):
                    value = mapping[id]
                    if type(value)==type(''):
                        proptype = tool.getPropertyType(id) or 'string'
                        if type_converters.has_key(proptype):
                            value = type_converters[proptype](value)
                        setattr(self, id, value)
        # call original
        MemberData._orig_setMemberProperties(self, mapping)

    MemberData._orig_setMemberProperties = MemberData.setMemberProperties
    MemberData.setMemberProperties = setMemberProperties



## Monkeypatch MembershipTool to search from member_catalog; used to be in custom tool
from Products.PlonePAS.tools.membership import MembershipTool

if not hasattr(MembershipTool, 'RhaptosSite_searchForMembers_patch'):
    logger.info("Patching PlonePAS.tools.membership.MembershipTool.searchForMembers")

    MembershipTool.RhaptosSite_searchForMembers_patch= 1

    import shlex
    from Products.AdvancedQuery import Eq, MatchGlob, Or, And

    def _cookZCSearchTerms(self, terms):
        catalog = getToolByName(self, 'member_catalog')
        lex = catalog.lexicon
        results = [' '.join(lex.parseTerms(term)) for term in terms]
        results = filter(None, results)

        # Remove duplicates
        uniq = {}
        for w in results:
            uniq[w] = 1

        return uniq.keys()

    MembershipTool._cookZCSearchTerms = _cookZCSearchTerms

    def searchForMembers( self, REQUEST=None, **kw ):
        """Search for users (not groups, not groups-as-users) of a site """
        if REQUEST:
            dict = REQUEST
        else:
            dict = kw

        name = dict.get('name', '')
        if name is None: name = ''  # Danger, Will Robinson! shlex.split(None), at least on some machines, hangs indefinitely!

        # Split up search terms but leave quoted ones together
        try:
            names = shlex.split(name)
        except ValueError:
            try:
                names = shlex.split(name.replace("'","\\'"))
            except ValueError:
                names = shlex.split(name.replace("'","\\'")+'"')

        # Short circuit: if all that was asked for was '*', just return everyone
        if names == ['*']:
            query = And()
        else:
            names = self._cookZCSearchTerms(names)
            queries = []
            for name in names:
                queries.extend([MatchGlob('fullname', name), MatchGlob('email', name), Eq('getUserName', name)])
            query = Or(*queries)
        #zLOG.LOG('MembershipTool', zLOG.BLATHER, 'Querying: %s' % query)

        catalog = getToolByName(self, 'member_catalog')
        return catalog.evalAdvancedQuery(query, ('surname', 'firstname'))
    
    MembershipTool._orig_searchForMembers= MembershipTool.searchForMembers
    MembershipTool.searchForMembers = searchForMembers




## Monkeypatch plone.py displayContentsTab to only display the tab if the type is in the
## site property 'use_folder_tabs'
## There might be a better way to override this is a Zope 3 mechanism, but we'll just monkeypatch it for now

# Adding IndexIterator to the correct path that it is expected inside CMFPlone.browser.plone,
# since we don't seem to have access to it otherwise from this context.
from Products import CMFPlone
from Products.CMFPlone.utils import IndexIterator
CMFPlone.IndexIterator = IndexIterator
from Products.CMFPlone.browser.plone import cache_decorator
from Products.CMFPlone.browser.plone import Plone
from Products.CMFCore.utils import _checkPermission

if not hasattr(Plone, 'RhaptosSite_patch'):
    logger.info("Patching CMFPlone.browser.plone.displayContentsTab")

    Plone.RhaptosSite_patch = 1
    
    from Products.CMFPlone.browser.plone import *     # get all the original's imports and definitions

    def displayContentsTab(self):
        """See interface"""
        context = utils.context(self)
        modification_permissions = (ModifyPortalContent,
                                    AddPortalContent,
                                    DeleteObjects,
                                    ReviewPortalContent)

        contents_object = context

        # If this object is the parent folder's default page, then the
        # folder_contents action is for the parent, we check permissions
        # there. Otherwise, if the object is not folderish, we don not display
        # the tab.
        if self.isDefaultPageInFolder():
            contents_object = self.getCurrentFolder()
        elif not self.isStructuralFolder():
            return 0

        # If this is not a structural folder, stop.
        plone_view = getMultiAdapter((contents_object, self.request),
                                     name='plone')
        if not plone_view.isStructuralFolder():
            return 0

        ## Begin monkeypatch
        prop_tool = getToolByName(context, 'portal_properties')
        use_ft = prop_tool.site_properties.getProperty('use_folder_tabs')
        if contents_object.portal_type not in use_ft:
            return 0
        ## End monkeypatch

        show = 0
        # We only want to show the 'contents' action under the following
        # conditions:
        # - If you have permission to list the contents of the relavant
        #   object, and you can DO SOMETHING in a folder_contents view. i.e.
        #   Copy or Move, or Modify portal content, Add portal content,
        #   or Delete objects.

        # Require 'List folder contents' on the current object
        if _checkPermission(ListFolderContents, contents_object):
            # If any modifications are allowed on object show the tab.
            for permission in modification_permissions:
                if _checkPermission(permission, contents_object):
                    show = 1
                    break

        return show

    Plone.displayContentsTab = cache_decorator(displayContentsTab)


## Monkeypatch the getObjSize index of the catalog to return None instead of "0 Kb" for empty objects
    
from Products.CMFPlone import CatalogTool
from Products.CMFPlone.CatalogTool import registerIndexableAttribute, _eioRegistry

if not hasattr(CatalogTool, 'RhaptosSite_patch'):
    logger.info("Patching CMFPlone.CatalogTool.getObjSize to say None instead of 0kb")

    CatalogTool.RhaptosSite_patch = 1

    from Products.CMFPlone.CatalogTool import *     # get all the original's imports and definitions
    
    def getObjSize(obj, **kwargs):
        """ Helper method for catalog based folder contents.

        >>> from Products.CMFPlone.CatalogTool import getObjSize

        >>> getObjSize(self.folder)
        '1 kB'
        """
        smaller = SIZE_ORDER[-1]

        if base_hasattr(obj, 'get_size'):
            size = obj.get_size()
        else:
            size = 0

        # if the size is a float, then make it an int
        # happens for large files
        try:
            size = int(size)
        except (ValueError, TypeError):
            pass

        if not size:
            return None

        if isinstance(size, (int, long)):
            if size < SIZE_CONST[smaller]:
                return '1 %s' % smaller
            for c in SIZE_ORDER:
                if size/SIZE_CONST[c] > 0:
                    break
            return '%.1f %s' % (float(size/float(SIZE_CONST[c])), c)
        return size

    _eioRegistry.unregister('getObjSize')
    registerIndexableAttribute('getObjSize', getObjSize)


## Monkeypatch the breadcrumbs to show the name of the page you're on, even if its the defult page
    
from Products.CMFPlone.browser.navigation import PhysicalNavigationBreadcrumbs

if not hasattr(PhysicalNavigationBreadcrumbs, 'RhaptosSite_patch'):
    logger.info("Patching CMFPlone.browser.navigation to include default page in breadcrumbs")

    PhysicalNavigationBreadcrumbs.RhaptosSite_patch = 1

    from Products.CMFPlone.browser.navigation import *     # get all the original's imports and definitions

    def breadcrumbs(self):
        context = utils.context(self)
        request = self.request
        container = utils.parent(context)
        
        try:
            name, item_url = get_view_url(context)
        except AttributeError:
            print context
            raise

        if container is None:
            return ({'absolute_url': item_url,
                     'Title': utils.pretty_title_or_id(context, context),
                    },)

        view = getMultiAdapter((container, request), name='breadcrumbs_view')
        base = tuple(view.breadcrumbs())

        #if base:                        # PATCH: broken for typesUseViewActionInListings; see get_view_url
        #    item_url = '%s/%s' % (base[-1]['absolute_url'], name)

        rootPath = getNavigationRoot(context)
        itemPath = '/'.join(context.getPhysicalPath())

        # don't show default pages in breadcrumbs or pages above the navigation root
        ## Begin monkeypatch
        if not rootPath.startswith(itemPath) and getattr(context.aq_explicit, 'Title', None):
        #if not utils.isDefaultPage(context, request) and not rootPath.startswith(itemPath):
        ## End monkeypatch
            base += ({'absolute_url': item_url,
                      'Title': utils.pretty_title_or_id(context, context),
                     },)

        return base

    PhysicalNavigationBreadcrumbs.breadcrumbs = breadcrumbs


## Don't create thumbnails for Images
## TODO: remove when uning UniFile exclusively
from Products.ATContentTypes.content.image import ATImage

if not hasattr(ATImage, 'RhaptosSite_no_thumbs_patch'):
    logger.info("Patching ATContentTypes.content.image to remove scales")

    ATImage.RhaptosSite_no_thumbs_patch = 1
    
    ATImage.schema['image'].sizes = None
    # generateMethods(ATImage, ATImage.schema.fields())


## Don't fail if getTypeInfo returns None, which is legal
## would make a good upstream contribution!
from Products.CMFPlone.browser.plone import Plone

if not hasattr(Plone, 'RhaptosSite_getTypeInfo_None_patch'):
    logger.info("Patching CMFPlone.browser.plone to fix _lookupTypeActionTemplate with getTypeInfo return of None")

    Plone.RhaptosSite_getTypeInfo_None_patch = 1
    
    def _lookupTypeActionTemplate(self, actionId):
        context = utils.context(self)
        fti = context.getTypeInfo()
        if fti is None:     # PATCH
            return None     # PATCH
        try:
            # XXX: This isn't quite right since it assumes the action starts with ${object_url}
            action = fti.getActionInfo(actionId)['url'].split('/')[-1]
        except ValueError:
            # If the action doesn't exist, stop
            return None

        # Try resolving method aliases because we need a real template_id here
        action = fti.queryMethodID(action, default = action, context = context)

        # Strip off leading /
        if action and action[0] == '/':
            action = action[1:]
        return action

    Plone._orig__lookupTypeActionTemplate = Plone._lookupTypeActionTemplate
    Plone._lookupTypeActionTemplate = _lookupTypeActionTemplate


## fix PluggableAuthService bug: causes users to be looked up by non-exact match criteria through getUserm
## which passes login to _verifyUser.
## This causes much havok in migration, searches, login, etc. For example, "getUser('Bar')" returns
## the user 'FooBar', because _verifyUser does an inexact match and finds ['FooBar', 'Bar'],
## and returns the first one!
## Backport from PAS trunk.
from Products.PluggableAuthService.PluggableAuthService import PluggableAuthService

if not hasattr(PluggableAuthService, 'RhaptosSite_verifyUser_patch'):
    logger.info("Patching PAS to fix stupid stupid non-exact-matching _verifyUser (and thus getUser)")
    from Products.PluggableAuthService.PluggableAuthService import createViewName, createKeywords
    from Products.PluggableAuthService.PluggableAuthService import IUserEnumerationPlugin

    PluggableAuthService.RhaptosSite_verifyUser_patch = 1

    def _verifyUser( self, plugins, user_id=None, login=None ):

        """ user_id -> info_dict or None
        """
        criteria = {'exact_match': True}  # <-- PATCH

        if user_id is not None:
            criteria[ 'id' ] = user_id

        if login is not None:
            criteria[ 'login' ] = login

        if criteria:
            view_name = createViewName('_verifyUser', user_id or login)
            keywords = createKeywords(**criteria)
            cached_info = self.ZCacheable_get( view_name=view_name
                                             , keywords=keywords
                                             , default=None
                                             )

            if cached_info is not None:
                return cached_info


            enumerators = plugins.listPlugins( IUserEnumerationPlugin )

            for enumerator_id, enumerator in enumerators:
                try:
                    info = enumerator.enumerateUsers( **criteria )

                    if info:
                        # Put the computed value into the cache
                        self.ZCacheable_set( info[0]
                                           , view_name=view_name
                                           , keywords=keywords
                                           )
                        return info[0]

                except _SWALLOWABLE_PLUGIN_EXCEPTIONS:
                    msg = 'UserEnumerationPlugin %s error' % enumerator_id
                    logger.debug(msg, exc_info=True)

        return None

    PluggableAuthService._orig__verifyUser = PluggableAuthService._verifyUser
    PluggableAuthService._verifyUser = _verifyUser




## Make sortable_title portal_catalog index act like title_or_id, so that sort looks right in the UI,
## which falls back to id in the event of a null Title.
from Products.CMFPlone import CatalogTool

if not hasattr(CatalogTool, 'RhaptosSite_sortable_title_patch'):
    logger.info("Patching Catalog Tool's sortable_title to act like title_or_id instead of Title")
    from Products.CMFPlone.CatalogTool import safe_callable, safe_unicode, num_sort_regex
    from Products.CMFPlone.CatalogTool import num_sort_regex
    from Products.CMFPlone.CatalogTool import registerIndexableAttribute

    CatalogTool.RhaptosSite_sortable_title_patch = 1

    def sortable_title(obj, portal, **kwargs):
        """ Helper method for to provide FieldIndex for Title.
    
        >>> from Products.CMFPlone.CatalogTool import sortable_title
    
        >>> self.folder.setTitle('Plone42 _foo')
        >>> sortable_title(self.folder, self.portal)
        'plone00000042 _foo'
        """
        title = getattr(obj, 'Title', None)
        if title is not None:
            if safe_callable(title):
                title = title()
        if not title:  # we want to catch empty string
            title = getattr(obj, 'getId', None)
            if title is not None and safe_callable(title):
                title = title()
            else:
                title = obj.id

        if isinstance(title, basestring):
            sortabletitle = title.lower().strip()
            # Replace numbers with zero filled numbers
            sortabletitle = num_sort_regex.sub(zero_fill, sortabletitle)
            # Truncate to prevent bloat
            sortabletitle = safe_unicode(sortabletitle)[:30].encode('utf-8')
            return sortabletitle
        return ''

    CatalogTool._orig_sortable_title = CatalogTool.sortable_title
    CatalogTool.sortable_title = sortable_title
    
    registerIndexableAttribute('sortable_title', sortable_title)


## Fix bug in MimeTypesRegistry.classify where it doesn't provide for a negative return from 'lookup'.
from Products.MimetypesRegistry.MimeTypesRegistry import MimeTypesRegistry

if not hasattr(MimeTypesRegistry, 'MimeTypesRegistry_classify_patch'):
    logger.info("Patching 'MimeTypesRegistry.classify' to fix bug in using 'lookup'")

    MimeTypesRegistry.MimeTypesRegistry_classify_patch = 1
    
    from Products.MimetypesRegistry.MimeTypesRegistry import magic, guess_content_type, aq_base

    def classify(self, data, mimetype=None, filename=None):
        """Classify works as follows:
        1) you tell me the rfc-2046 name and I give you an IMimetype
           object
        2) the filename includes an extension from which we can guess
           the mimetype
        3) we can optionally introspect the data
        4) default to self.defaultMimetype if no data was provided
           else to application/octet-stream of no filename was provided,
           else to text/plain

        Return an IMimetype object or None 
        """
        mt = None
        if mimetype:
            mt = self.lookup(mimetype)
            if mt:
                mt = mt[0]
        elif filename:
            mt = self.lookupExtension(filename)
            if mt is None:
                mt = self.globFilename(filename)
        if data and not mt:
            for c in self._classifiers():
                if c.classify(data):
                    mt = c
                    break
            if not mt:
                mstr = magic.guessMime(data)
                if mstr:
                    #mt = self.lookup(mstr)[0]   ### <---- bug
                    ## PATCH...
                    lookup = self.lookup(mstr)
                    if lookup:
                        mt = lookup[0]
                    ## DONE
        if not mt:
            if not data:
                mtlist = self.lookup(self.defaultMimetype)
            elif filename:
                mtlist = self.lookup('application/octet-stream')
            else:
                failed = 'text/x-unknown-content-type'
                filename = filename or ''
                data = data or ''
                ct, enc = guess_content_type(filename, data, None)
                if ct == failed:
                    ct = 'text/plain'
                mtlist = self.lookup(ct)
            if len(mtlist)>0:
                mt = mtlist[0]
            else:
                return None

        # Remove acquisition wrappers
        return aq_base(mt)

    MimeTypesRegistry._orig_classify = MimeTypesRegistry.classify
    MimeTypesRegistry.classify = classify

## Set profile image to scale on upload to 150x150, instead of default 75x100
logger.info("Patching 'CMFPlone.utils' to change member profile image scaling")
from Products.CMFPlone import utils
MEMBER_IMAGE_SCALE = (150, 150)
utils.IMAGE_SCALE_PARAMS['scale'] = MEMBER_IMAGE_SCALE


## backport CMFPlone.patches.unicodehacks.FasterStringIO for CacheFu problem
## needed for source_create not to explode with a plain restrictedTraverse with non-ASCII data
## see http://plone.org/products/cachefu/issues/126 and
##     http://dev.plone.org/collective/changeset/67165 for reason
# see http://svn.plone.org/svn/plone/Plone/trunk/Products/CMFPlone/patches/unicodehacks.py for code
from Products.PageTemplates.PageTemplate import PageTemplate

if not hasattr(PageTemplate, 'FasterStringIO_patch'):
    logger.info("Patching Products.PageTemplates.PageTemplate to use backported CMFPlone.unicodehacks StringIO")

    PageTemplate.FasterStringIO_patch = 1

    from collections import deque

    def _unicode_replace(structure):
        if isinstance(structure, str):
            text = structure.decode('utf-8', 'replace')   # PATCH: error handling specified to deal with binary
        else:
            text = unicode(structure)
        return text

    class FasterStringIO(object):
        """Append-only version of StringIO, which ignores any initial buffer.

        Implemented by using an internal deque instead.
        """
        def __init__(self, buf=None):
            self.buf = buf = deque()
            self.bufappend = buf.append

        def close(self):
            self.buf.clear()

        def seek(self, pos, mode=0):
            raise RuntimeError("FasterStringIO.seek() not allowed")

        def write(self, s):
            self.bufappend(s)

        def getvalue(self):
            buf = self.buf
            try:
                result = u''.join(buf)
            except UnicodeDecodeError:
                result = u''.join([_unicode_replace(value) for value in buf])
            buf.clear()
            return result.encode('utf-8')   # PATCH: output regular strings, to avoid any more unicode surprises

    PageTemplate._orig_StringIO = PageTemplate.StringIO
    PageTemplate.StringIO = FasterStringIO
