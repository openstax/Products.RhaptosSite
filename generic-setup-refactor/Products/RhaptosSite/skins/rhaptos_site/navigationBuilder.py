# Create data structure for our limited navigation tree, which should be much simpler
# and faster than the default generic one.
# This works on the following rules:
#  - it will display only two levels
#  - it will not exist for the root (tabs will take us to the root's children, the main sections)
#  - it will display all the contents of a section (off of root) all the time
#  - when viewing a component in a section, it will be highlighted
#  - if a component in a section has contents, show those while that component is in the path
#     unless it has child named 'forcecollapse' (a special object that will never be shown)
#  - never show more than two levels
#  - when viewing deeper than a child of a section (of a portal root object), highlight only the
#    child of a section
# Note that we are NOT recursive!

COLLAPSE_SPECIAL_ID = 'forcecollapse'

portal = context.portal_url.getPortalObject()
catalog = context.portal_catalog

portalpath = portal.getPhysicalPath()  # /plone
portallen = len(portalpath)  # usually 2

contextpath = context.getPhysicalPath()
contextlen = len(contextpath)

secpathlen = portallen+1   # usually 3
compathlen = portallen+2   # usually 4
itempathlen = portallen+3  # usually 5

contextsection = contextlen >= secpathlen and contextpath[:secpathlen]   # ('', 'plone', 'aboutus')
contextcomponent = contextlen >= compathlen and contextpath[:compathlen] # ('', 'plone', 'aboutus', 'technology')
currentitem = contextlen >= itempathlen and contextpath[:itempathlen] or contextcomponent or None

#noListTypes = portal.portal_properties.navtree_properties.metaTypesNotToList  # has meta_types, not portal
noListTypes = ('Image', 'User Feedback')

#print portalpath
#print contextpath
#print contextsection
#print contextcomponent
#print currentitem
#print

if not contextsection:
    return None

#interesting = [x for x in catalog(path='/'.join(contextsection))
#               if (len(x.getPath().split('/')) == 4) or x.getPath().split('/')]

interesting = []
for elt in catalog(path={'query':'/'.join(contextsection), 'depth':1},
                   review_state='published', sort_on='getObjPositionInParent'):
    p = tuple(elt.getPath().split('/'))

    ## subtree...
    next = []
    expand = False
    if p == contextcomponent:
        collapse = catalog(path='/'.join(contextcomponent+(COLLAPSE_SPECIAL_ID,)))
        if not collapse: # ...the default case
            for nextelt in catalog(path={'query':'/'.join(contextcomponent), 'depth':1},
                                   review_state='published',sort_on='getObjPositionInParent'):
                p2 = tuple(nextelt.getPath().split('/'))
                if nextelt.Type not in noListTypes and p2[-1] != COLLAPSE_SPECIAL_ID:
                    next.append({'elt':nextelt, 'current':currentitem == p2})

    if elt.Type not in noListTypes:
        interesting.append({'elt':elt, 'subtree':next, 'current':currentitem == tuple(p)})
        
# debugging: text output!
#print '----------'
#for record in interesting:
    #brain = record['elt']
    #expanded = record['subtree']
    #current = record['current']
    #print ' -', brain.getPath().split('/')
    #if current: print "^^^"
    #if expanded:
        #for subrecord in expanded:
            #subbrain = subrecord['elt']
            #subcurrent = subrecord['current']
            #print '  *', subbrain.getPath().split('/')
            #if subcurrent: print "^^^"
#return printed
#context.plone_log(printed)

return interesting