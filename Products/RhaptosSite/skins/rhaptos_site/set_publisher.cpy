## Script (Python) ""
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=users=[]
##title=Set Publisher
##

from Products.CMFPlone import PloneMessageFactory as _

users = context.REQUEST['users']
acl_users = context.acl_users
mtool = context.portal_membership
getMemberById = mtool.getMemberById

for user in users:
            member = getMemberById(user)
            acl_users.userFolderEditUser(user, None, member.getRoles()+['Publisher'], member.getDomains(), REQUEST=context.REQUEST)

context.plone_utils.addPortalMessage(_(u'Changes applied.'))
context.plone_utils.addPortalMessage(', '.join(users))
return state
