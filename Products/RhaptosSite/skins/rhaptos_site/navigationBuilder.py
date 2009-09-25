# Create data structure for our limited navigation tree, which should be much simpler
# and faster than the default generic one.
# This works on the following rules:
#  - it will display only two levels
#  - it will not exist for the root (tabs will take us to the root's children, the main sections)
#  - it will display all the contents of a section (off of root) all the time
#  - when viewing a component in a section, it will be highlighted
#  - if a component in a section has contents, show those while that component is in the path
#  - never show more than two levels
#  - when viewing deeped than a child of a section (of a portal root object), highlight only the
#    child of a section
# Note that we are NOT recursive!
# TODO: a lot of the checking for paths of a certain level could be eliminated by
#       use of AdvancedQuery, probably

# this is stupid; it should get it from a property or something, but this will have to do...
expandoWhitelist = (
                    (r'/plone/aboutus/people'),
                    (r'/plone/aboutus/technology')
                    )
expandoWhitelist = [tuple(x.split('/')) for x in expandoWhitelist]

portal = context.portal_url.getPortalObject()
catalog = context.portal_catalog

portalpath = portal.getPhysicalPath()
contextpath = context.getPhysicalPath()

contextlen = len(contextpath)
contextsection = contextlen >= 3 and contextpath[:3]
contextcomponent = contextlen >= 4 and contextpath[:4]
currentitem = contextlen >= 5 and contextpath[:5] or contextcomponent or None

#noListTypes = portal.portal_properties.navtree_properties.metaTypesNotToList  # has meta_types, not portal
noListTypes = ('Image', 'User Feedback')

#print portalpath
#print contextpath, contextsection, contextcomponent
#print currentitem
#print

if not contextsection:
    return None

#interesting = [x for x in catalog(path='/'.join(contextsection))
#               if (len(x.getPath().split('/')) == 4) or x.getPath().split('/')]

interesting = []
for elt in catalog(path='/'.join(contextsection), review_state='published', sort_on='getObjPositionInParent'):
    p = tuple(elt.getPath().split('/'))
    l = len(p)

    next = None
    if l == 4:
        #print '-', l, '-', p
        ## subtree...
        if tuple(p[:4]) == contextcomponent:
            next = []
            for nextelt in catalog(path='/'.join(contextcomponent),
                                   review_state='published',sort_on='getObjPositionInParent'):
                p2 = tuple(nextelt.getPath().split('/'))
                l2 = len(p2)
                #print '--', l2, '-', p2, '++', p in expandoWhitelist, '/', expandoWhitelist
                if l2 == 5 and p in expandoWhitelist:
                    if nextelt.Type not in noListTypes:
                        next.append({'elt':nextelt, 'current':currentitem == p2})
        #print elt.id, elt.Type, elt.portal_type
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