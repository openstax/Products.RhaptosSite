## Script (Python) ""
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=users=[], resetpassword=[], delete=[], delete_member_area=[]
##title=Edit users
##

from Products.CMFPlone import PloneMessageFactory as _

# Rhaptos note: overridden from CMFPlone for memberarea deletion and uncataloging

acl_users = context.acl_users
mtool = context.portal_membership
mcat = context.member_catalog
getMemberById = mtool.getMemberById
mailPassword = context.portal_registration.mailPassword
setMemberProperties = context.plone_utils.setMemberProperties
generatePassword = context.portal_registration.generatePassword

for user in users:
    # Don't bother if the user will be deleted anyway
    if user.id in delete:
        continue

    member = getMemberById(user.id)
   # If email address was changed, set the new one
    if hasattr(user, 'email'):
        # If the email field was disabled (ie: non-writeable), the
        # property might not exist.
        if user.email != member.getProperty('email'):
            setMemberProperties(member, email=user.email)

    # If reset password has been checked email user a new password
    if hasattr(user, 'resetpassword'):
        pw = generatePassword()
    else:
        pw = None
        
    acl_users.userFolderEditUser(user.id, pw, user.get('roles',[]), member.getDomains(), REQUEST=context.REQUEST)
    if pw:
        context.REQUEST.form['new_password'] = pw
        mailPassword(user.id, context.REQUEST)

if delete:
    for u in delete:
        mcat.uncatalog_object(mcat(getUserName=u)[0].getPath())

    if delete_member_area:
        for m in delete_member_area:
            delete.remove(m)
        mtool.deleteMembers(delete_member_area, delete_memberareas=1, delete_localroles=1, REQUEST=context.REQUEST)

    mtool.deleteMembers(delete, delete_memberareas=0, delete_localroles=1, REQUEST=context.REQUEST)



context.plone_utils.addPortalMessage(_(u'Changes applied.'))
return state
