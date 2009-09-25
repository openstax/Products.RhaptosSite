## Script (Python) "wgforcontent"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=contentpath, wgcache={}, wglist=None
##title=get workspace/workgroup object from string representing content

## Rhaptos note: no plone counterpart.

# Provide string path to content, and get workspace/workgroup object back.
# Provide list of good groups, so we can check we're seeing the right thing.
#  Default to generating this list each call.
# Pass a dictionary 'wgcache' to preserve WG results between multiple calls.
#  Default is looking up each WG each time.

from Products.CMFCore.utils import getToolByName
from AccessControl import Unauthorized
urltool = getToolByName(context, 'portal_url')
portal = urltool.getPortalObject()

if not wglist:
    mtool = getToolByName(context, 'portal_membership')
    gtool = getToolByName(context, 'portal_groups')
    member = mtool.getAuthenticatedMember()
    wglist = gtool.getGroupsForPrincipal(member)

splitpath = contentpath.split('/')
splitpath = splitpath[:-1]   # chop the end off, which should be the editor object
wg = None
while 1:   # fake do/while loop walks up the path looking for WGs
    strpath = '/'.join(splitpath)
    wg = wgcache.get(strpath, None)  # retrieve from store to avoid extra work, if possible
    if wgcache.has_key(strpath):
        break
    else:
        candidate = portal.restrictedTraverse(splitpath)
        if candidate and candidate.portal_type in ('Workgroup', 'Workspace'):
            # first, make sure it one of user's WGs...
            unauth = 0
            try:
                if candidate.portal_type == 'Workgroup' and candidate.getId() not in wglist:
                    unauth = 1    # not one of our WGs, some oddity in catalog results
            except Unauthorized:   # commonly fails on getId
                unauth = 1
            if unauth:
                wgcache[strpath] = None  # record failures also
                break
            
            # set and store
            wg = candidate
            wgcache[strpath] = wg
        else:
            splitpath = splitpath[:-1]

        # exit condition:
        if wg or len(splitpath) <= 1:  # splitpath of 1 is portal (or above), and that's far enough
            break
return wg
