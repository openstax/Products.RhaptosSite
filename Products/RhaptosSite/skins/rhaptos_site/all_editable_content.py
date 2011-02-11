## Script (Python) "all_editable_content"
## nee "getRecentlyModified"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=limit=0, sort=None, sort_order=None, types=None
##title= Returns a list of the current member's modules and collections regardless of location
# 'limit' is number of recognizable 
# 'sort' is portal_catalog sort_on key; default is title (sortable_title). 'modified' accepted.
# 'sort_order' is, similarly, portal_catalog order key. 'ascending' is default, unless sort is 'modified,
#     then 'descending'.
# 'types' is list of portal_catalog types to retrieve; limited to 'Module' and 'Collection'. default is both.
# Returns list of dicts with info about the content and its location.

## Rhaptos note: no plone counterpart.
from Products.RhaptosSite.managercatalog import workspacesSearchResults

sort = sort or 'sortable_title'
types = types or ['Module','Collection']
sort_order = sort_order or (sort=='modified' and 'descending') or 'ascending'

from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName

urltool = getToolByName(context, 'portal_url')
ctool = getToolByName(context, 'portal_catalog')
repos = getToolByName(context, 'content')
mtool = getToolByName(context, 'portal_membership')
gtool = getToolByName(context, 'portal_groups')

portalurl = urltool()
portalpath = urltool.getPortalPath()       # /plone
lenportalpath = len(portalpath)
gpath = "%s/workgroups" % (portalpath)

member = mtool.getAuthenticatedMember()
wglist = gtool.getGroupsForPrincipal(member)
mpath = "%s/%s/%s" % (portalpath, mtool.membersfolder_id,member)

knownwgs = {}  # keep found WGs around, to avoid extra restrictedTraverses

rawresults = workspacesSearchResults(ctool, portal_type=types, sort_on=sort, sort_order=sort_order, path=[mpath,gpath])
# FIXME: for Managers, this will list everything

results = []
count = 0
for brain in rawresults:
    bpath = brain.getPath()          # /plone/Members/jccooper/m9000

    # short-circuit bad data
    if bpath.rfind('/portal_factory/') != -1:
        continue

    # find WG location
    workspacegroup = context.wgforcontent(bpath, knownwgs, wglist)
    if workspacegroup == None:
        continue

    # prepare data
    c_url = bpath
    if c_url.startswith(portalpath):
        c_url = c_url[lenportalpath:]
    c_url = ''.join((portalurl, c_url))

    c_id = brain.getId
    c_published = False
    if repos.hasRhaptosObject(c_id):    # TODO: having objectId as catalog field would be better
        c_published = True

    # format data
    results.append( {'content_portal_type':brain.portal_type,
                     'content_path':bpath,
                     'content_url':c_url,
                     'content_id':c_id,
                     'content_published':c_published,
                     'content_title':brain.Title,
                     'content_modified':brain.modified,
                     'work_portal_type':workspacegroup.portal_type,
                     'work_url':workspacegroup.absolute_url(),
                     'work_title':workspacegroup.Title()} )
    count += 1
    if limit > 0 and count > limit-1:
        break

return results
