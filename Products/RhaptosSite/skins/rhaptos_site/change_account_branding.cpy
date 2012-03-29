## Script (Python) "change_account_branding.cpy"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=checked_now=[], checked_initial=[], perma_now=[], perma_initial=[] 
##title=Change account branding
##

add_branding     = [branding_now for branding_now in checked_now
                    if len(branding_now) > 0 and branding_now not in checked_initial]
removed_branding = [branding_initial for branding_initial in checked_initial
                    if len(branding_initial) > 0 and branding_initial not in checked_now]
add_perma     = [perma for perma in perma_now
                    if len(perma) > 0 and perma not in perma_initial]
removed_perma = [perma for perma in perma_initial
                    if len(perma) > 0 and perma not in perma_now]

#context.plone_log('account to add branding:\n%s'    % str(add_branding))
#context.plone_log('account to remove branding:\n%s' % str(removed_branding))

from Products.CMFCore.utils import getToolByName
portal = context.portal_url.getPortalObject()
mtool = getToolByName(portal, "portal_membership")

for add_account_id in add_branding:
    acl_user = mtool.getMemberById(add_account_id)
    roles = acl_user.getRoles()
    if 'Branding' not in roles:
        roles.append('Branding')
        portal.acl_users.userFolderEditUser(add_account_id,None,roles)
    if add_account_id in add_perma and 'PermaBranding' not in roles:
        roles.append('PermaBranding')
        portal.acl_users.userFolderEditUser(add_account_id,None,roles)

for remove_account_id in removed_branding:
    acl_user = mtool.getMemberById(remove_account_id)
    roles = acl_user.getRoles()
    if 'Branding' in roles:
        roles.remove('Branding')
        portal.acl_users.userFolderEditUser(remove_account_id,None,roles)

for remove_account_id in removed_perma:
    acl_user = mtool.getMemberById(remove_account_id)
    roles = acl_user.getRoles()
    if 'PermaBranding' in roles:
        roles.remove('PermaBranding')
        portal.acl_users.userFolderEditUser(remove_account_id,None,roles)

return state.set(status='success')
