## Script (Python) ""
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Set Publishable
##

from Products.CMFPlone import PloneMessageFactory as _

# Rhaptos note: overridden from CMFPlone for memberarea deletion and uncataloging

acl_users = context.acl_users
mtool = context.portal_membership
getMemberById = mtool.getMemberById
rep = context.content

modusers=[]
users = mtool.listMemberIds()
for user in users:
    for r in ['maintainer','author','licensor']:
        if rep.getContentByRole(r,user):
            modusers.append(user)
            member = getMemberById(user)
            acl_users.userFolderEditUser(user, None, member.getRoles()+['Publisher'], member.getDomains(), REQUEST=context.REQUEST)
            break

context.plone_utils.addPortalMessage(_(u'Changes applied.'))
context.plone_utils.addPortalMessage(', '.join(modusers))
return state
