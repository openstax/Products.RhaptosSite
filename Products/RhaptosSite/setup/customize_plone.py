from Products.CMFCore.utils import getToolByName

def setActions(context):
    """ Modify the default Plone actions
    """
    site = context.getSite()
    logger = context.getLogger('actions')
    acttool = getToolByName(site, 'portal_actions')

    #  ...turn off new site actions, and change_state (which was added, different from older change_status)
    actions = acttool._cloneActions()
    #import pdb; pdb.set_trace()
    bug_index = 0
    contact_action = None
    for a in actions:
        if a.id == 'sitemap':
            a.visible = 0
        elif a.id == 'accessibility':
            a.visible = 0
        elif a.id == 'change_state':
            a.visible = 0
        elif a.id == 'full_screen':
            a.visible = 0
        elif a.id == 'Members' and a.title == 'Authoring Area':
            a.visible = 1
        elif a.id == 'contact':
            a.title = 'Contact Us'
            # There may not be an aboutus folder in a default site... should this go somewhere else?
            #a.action = Expression("string:${portal_url}/aboutus/contact")
            contact_action = a
        elif a.id == 'bugreport':
            bug_index = actions.index(a)

    try:
        actions.remove(contact_action)
    except ValueError:
        # We don't care if its not here
        pass
    actions.insert(bug_index,contact_action)
    acttool._actions = tuple(actions)

    # Also, turn off auto-tabs-from-top-level-content
    proptool = getToolByName(site, 'portal_properties')
    proptool.site_properties.manage_changeProperties(disable_folder_sections=1)
    
    logger.info('Actions set.')
