from Products.Archetypes.Extensions.utils import install_subskin
from Products.RhaptosSite import product_globals as GLOBALS
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression
from zExceptions import BadRequest


def memberfoldertitle(folder):
    """Get the current system default title for a member folder (workspace).
    Relies on presence of REQUEST; if calling from script/debug,
    use Testing.makerequest.makerequest first.
    See 'MembershipTool.createMemberArea'
    """
    translation_service = getToolByName(folder, 'translation_service')
    sampleid = folder.getId()
    umember_id = translation_service.asunicodetype(sampleid, errors='replace')
    return translation_service.utranslate(domain='plone', msgid='title_member_folder',
                                          mapping={'member': umember_id},  context=folder, target_language='en')


def install(context):
    """Set up RhaptosSite: register with the necessary tools, etc.
    """
    logger = context.getLogger('rhaptossite')
    if context.readDataFile('rhaptossite.txt') is None:
        logger.info('Nothing to import')
        return
    portal = context.getSite()
    logger.info("Starting RhaptosSite install")
    groups_tool = getToolByName(portal, 'portal_groups')
    
    
    
    # Make workflow go away
    logger.info("...making workflow empty")
    wf_tool = getToolByName(portal,'portal_workflow')
    wf_tool.setChainForPortalTypes(['UnifiedFile'],'')
    
    ## create 'mydashboard' folder, mostly just to get it in the path
    # its default vew is 'author_home'
    mydashboard = getattr(portal, 'mydashboard', None)
    if not mydashboard:
        logger.info("...creating 'mydashboard' folder")
        portal.invokeFactory('Folder', id="mydashboard", title="MyCNX")
        mydashboard = getattr(portal, 'mydashboard', None)
    mydashboard.layout = "author_home"
    
    cachetool = getToolByName(portal,'portal_cache_settings', None)
    # GenericSetup has a cache policy, but we've backported and it doesn't quite work with our versions
    # when we upgrade, this should probably be replaced with a 'cachesettings.xml' (though it'll be)
    # a little less flexible (no getActivePolicy), and we'll still need to do ordering probably
    if cachetool:
        mydashboardruleid = 'mydashboard-rule'
        policy = cachetool[cachetool.getActivePolicyId()]
        rulesfolder = policy.rules
        mydashboardrule = getattr(rulesfolder, mydashboardruleid, None)
        if not mydashboardrule:
            rulesfolder.invokeFactory('ContentCacheRule', id=mydashboardruleid, title='mydashboard no-cache')
            mydashboardrule = getattr(rulesfolder, mydashboardruleid)
        mydashboardrule.setDescription("The '/mydashboard' object shows dynamic data and should not be cached.")
        mydashboardrule.setContentTypes(['Folder'])
        mydashboardrule.setDefaultView(True)
        mydashboardrule.setPredicateExpression("python:object.getId()=='mydashboard'")
        mydashboardrule.setHeaderSetIdAnon('no-cache')
        mydashboardrule.setHeaderSetIdAuth('no-cache')
        rulesfolder.moveObject(mydashboardruleid, 0)
        
    left_slots = ['context/workspaces_slot/macros/portlet',]
    try:
        mydashboard.manage_addProperty('left_slots', left_slots, type='lines')
    except BadRequest:
        mydashboard.manage_changeProperties(left_slots=left_slots)

    right_slots = ['context/portlet_login/macros/portlet',
                   'context/portlet_loggedin/macros/portlet',
                   'context/portlet_recentview/macros/portlet']
    try:
        mydashboard.manage_addProperty('right_slots', right_slots, type='lines')
    except BadRequest:
        mydashboard.manage_changeProperties(right_slots=right_slots)

    ## set slot properties
    logger.info("...setting slot properties")
    # set the right slots for member workspace and the workgroups
    # log_action_slot portlet is only seen in the module/collection context
    # portlet_recentview is only seen in the workspace/workgroup context

    right_slots = ['context/portlet_login/macros/portlet',
                   'context/portlet_loggedin/macros/portlet',
                   'context/log_action_slot/macros/portlet',]

    members = portal.Members
    try:
        members.manage_addProperty('right_slots', right_slots, type='lines')
    except BadRequest:
        members.manage_changeProperties(right_slots=right_slots)

    workgroups = groups_tool.getGroupWorkspacesFolder()
    try:
        workgroups.manage_addProperty('right_slots', right_slots, type='lines')
    except BadRequest:
        workgroups.manage_changeProperties(right_slots=right_slots)

    # delete unwanted actions
    # FIXME: when GenericSetup actions handler allows remove="True", do this in the profile
    pa_tool = getToolByName(portal, 'portal_actions')
    actlist = pa_tool.listActions()
    actindex = -1
    actfound = None
    for act in actlist:
        if not actfound: actindex += 1
        if act.id == 'author_home':
            actfound = True
    if actfound:
        logger.info("Removing action 'author_home'")
        pa_tool.deleteActions([actindex])

    ## upgrades
    logger.info("...upgrades (if necessary)")
    
    # check for members folder rename
    m_tool = getToolByName(portal, 'portal_membership')
    membersfolder = m_tool.getMembersFolder()
    members = None
    sample = getattr(membersfolder, 'jccooper', None)
    if not sample:
        members = membersfolder.objectValues()
        if members:
            sample = members[0]
    if sample:  # else we have no members: new site
        newtitle = memberfoldertitle(sample)
        if sample.Title() != newtitle:
            logger.info("- upgrading personal workspace titles")
            oldpatterntitle = "%s's Workspace"  # can't actually get this, so hard-code it
            members = members or membersfolder.objectValues()
            for f in members:
                oldtitle = f.Title()
                newtitle = memberfoldertitle(f)
                f.setTitle(newtitle)
                #logger.info(f.getId())
                if oldtitle != oldpatterntitle % f.getId():  # prepend old custom title to description
                    desc = f.Description()
                    f.setDescription(oldtitle + ": " + desc)
            logger.info("< done")

    # remove unnecessary portal_catalog indexes
    cat = getToolByName(portal,'portal_catalog')
    existing_indexes = cat.indexes()
    keep_indexes = ['Creator', 'portal_type', 'allowedRolesAndUsers', 'orig_id', 'review_state', 
                    'path', 'getObjPositionInParent', 'sortable_title', 'modified', 'created', 
                    'Date', 'effectiveRange']

    for i in keep_indexes:
        existing_indexes.remove(i)
    logger.info("Removing excess portal_catalog indexes")
    cat.manage_delIndex(existing_indexes)

    logger.info("Successfully installed %s." % 'RhaptosSite')
