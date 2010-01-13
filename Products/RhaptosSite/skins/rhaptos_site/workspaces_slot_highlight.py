## Script (Python) "workspaces_slot_highlight"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=template, home, rhaptosobj, lensfolder_url
##title=Determine highlight location in workspaces_slot
##

# returns value for category and element to highlight as tuple (cat, elt)

request = context.REQUEST
templateid = template.getId()
current_url = request.URL
ppath = context.getPhysicalPath()
orig_template = request.get('orig_template', None)

# note: order matters in some places, here.
# 'editobj' for example, should stop any location highlights, and does so by coming before them.
# 'listcontent' is called in context of 'mycnx', so it comes before that.
# and a few other. In other words, tread carefully.

if templateid == 'listcontent' or orig_template and orig_template.startswith('listcontent'):
    # by type: modules/collections
    section = []
    contentparams = request.get('type', None) or orig_template.split('?')[1]
    if 'Module' in contentparams:
        section.append('module')
    if 'Collection' in contentparams:
        section.append('collection')
    return 'bytype', section
elif templateid in ('manageworkgroups', 'create_workgroup'):
    # by location: special action
    return 'bylocationaction', templateid
elif templateid == 'author_home' or 'mycnx' in ppath or '/mycnx/' in current_url:
    # mycnx/home (anything in mycnx not already found above, incl. context-less creation)
    return 'home', None
elif current_url.startswith(lensfolder_url.split('?')[0]) or templateid == 'lens_edit':  #template check for creation
    # by type: lenses
    return 'bytype', 'lens'
elif rhaptosobj and not context.portal_factory.isTemporary(rhaptosobj):
    # on some (concrete) editor object
    return 'editobj', None
else:
    homepath = home and home.getPhysicalPath() or None
    if homepath and ppath[:len(homepath)]==homepath:
        # by location: workspace
        return 'bylocationpersonal', None
    gwpath = context.portal_groups.getGroupWorkspacesFolder().getPhysicalPath()
    if ppath[:len(gwpath)]==gwpath:
        # by location: workgroup
        return 'bylocationgroup', None  # cannot know group name here; template will check as it loops

return None, None