# -*- coding: utf-8 -*-
"""GenericSetup setup handlers for RhaptosSite."""
from zExceptions import BadRequest
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression
from Products.Archetypes.Extensions.utils import install_subskin
from plone.app.controlpanel.security import ISecuritySchema

from Products.RhaptosSite import product_globals as GLOBALS
from Products.RhaptosSite.setup.RhaptosSetup import functions


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


def set_up_security(site):
    """Enable/disable security controlpanel (a.k.a. @@security-controlpanel)
    settings."""
    security = ISecuritySchema(site)
    #: Enable self registration (member join process).
    security.enable_self_reg = True


def install(context):
    """Set up RhaptosSite: register with the necessary tools, etc.
    """
    logger = context.getLogger('rhaptossite')
    if context.readDataFile('rhaptossite.txt') is None:
        logger.info('Nothing to import')
        return
    portal = context.getSite()

    # XXX Directly calling the setup functions. There is likely a better
    #     way to do this; and it's called GenericSetup export/import adapters.
    for title, func in functions:
        logger.info("Running setup function for %s." % title)
        func(context, portal)

    logger.info("Starting RhaptosSite install")
    groups_tool = getToolByName(portal, 'portal_groups')

    set_up_security(portal)

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
