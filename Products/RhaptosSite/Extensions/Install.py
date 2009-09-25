from Products.Archetypes.Extensions.utils import install_subskin
from Products.RhaptosSite import product_globals as GLOBALS
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression
from zExceptions import BadRequest

from cStringIO import StringIO

import logging
logger = logging.getLogger('RhaptosSite.Install')
def log(msg, out=None):
    logger.info(msg)
    if out: print >> out, msg
    print msg

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


def install(self):
    """Set up RhaptosSite: register with the necessary tools, etc.
    """
    out = StringIO()
    log("Starting RhaptosSite install", out)
    portal = self.portal_url.getPortalObject()
    groups_tool = getToolByName(portal, 'portal_groups')
    
    setup_tool = getToolByName(portal, 'portal_setup')
    prevcontext = setup_tool.getImportContextID()
    setup_tool.setImportContext('profile-CMFPlone:plone')  # get Plone steps registered
    setup_tool.setImportContext('profile-RhaptosSite:rhaptos-default') # Rhaptos steps registered
    # FIXME: in the future, we would like to just run all steps. the existing steps, however,
    # are probably not re-install safe
    
    # run all import steps
    steps = ('actions','typeinfo','jsregistry','rhaptos_cmfformcontroller')
    log("...running profile steps", out)
    for step in steps:
        log(" - applying step: %s" % step, out)
        status = setup_tool.runImportStep(step)
        log(status['messages'][step], out)
    # see Upgrades/up112_113.zctl where a lot of actions got set up
    log("...profile steps done", out)
    
    ## "tear down" generic setup
    setup_tool.setImportContext(prevcontext)
    
    # Make workflow go away
    log("...making workflow empty", out)
    wf_tool = getToolByName(self,'portal_workflow')
    wf_tool.setChainForPortalTypes(['UnifiedFile'],'')
    
    ## create 'mycnx' folder, mostly just to get it in the path
    # its default vew is 'author_home'
    mycnx = getattr(portal, 'mycnx', None)
    if not mycnx:
        log("...creating 'mycnx' folder", out)
        portal.invokeFactory('Folder', id="mycnx", title="MyCNX")
        mycnx = getattr(portal, 'mycnx', None)
    mycnx.layout = "author_home"
    
    cachetool = getToolByName(self,'portal_cache_settings', None)
    # GenericSetup has a cache policy, but we've backported and it doesn't quite work with our versions
    # when we upgrade, this should probably be replaced with a 'cachesettings.xml' (though it'll be)
    # a little less flexible (no getActivePolicy), and we'll still need to do ordering probably
    if cachetool:
        mycnxruleid = 'mycnx-rule'
        policy = cachetool[cachetool.getActivePolicyId()]
        rulesfolder = policy.rules
        mycnxrule = getattr(rulesfolder, mycnxruleid, None)
        if not mycnxrule:
            rulesfolder.invokeFactory('ContentCacheRule', id=mycnxruleid, title='MyCNX no-cache')
            mycnxrule = getattr(rulesfolder, mycnxruleid)
        mycnxrule.setDescription("The '/mycnx' object shows dynamic data and should not be cached.")
        mycnxrule.setContentTypes(['Folder'])
        mycnxrule.setDefaultView(True)
        mycnxrule.setPredicateExpression("python:object.getId()=='mycnx'")
        mycnxrule.setHeaderSetIdAnon('no-cache')
        mycnxrule.setHeaderSetIdAuth('no-cache')
        rulesfolder.moveObject(mycnxruleid, 0)
        
    left_slots = ['context/workspaces_slot/macros/portlet',]
    try:
        mycnx.manage_addProperty('left_slots', left_slots, type='lines')
    except BadRequest:
        mycnx.manage_changeProperties(left_slots=left_slots)

    right_slots = ['context/portlet_login/macros/portlet',
                   'context/portlet_loggedin/macros/portlet',
                   'context/portlet_recentview/macros/portlet']
    try:
        mycnx.manage_addProperty('right_slots', right_slots, type='lines')
    except BadRequest:
        mycnx.manage_changeProperties(right_slots=right_slots)

    ## set slot properties
    log("...setting slot properties", out)
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
        log("Removing action 'author_home'", out)
        pa_tool.deleteActions([actindex])

    ## upgrades
    log("...upgrades (if necessary)", out)
    
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
            log("- upgrading personal workspace titles", out)
            oldpatterntitle = "%s's Workspace"  # can't actually get this, so hard-code it
            members = members or membersfolder.objectValues()
            for f in members:
                oldtitle = f.Title()
                newtitle = memberfoldertitle(f)
                f.setTitle(newtitle)
                #log(f.getId(), out)
                if oldtitle != oldpatterntitle % f.getId():  # prepend old custom title to description
                    desc = f.Description()
                    f.setDescription(oldtitle + ": " + desc)
            log("< done", out)
    log("Successfully installed %s." % 'RhaptosSite', out)
    return out.getvalue()
