## Script (Python) ""
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Set Publisher
##

mtool = context.portal_membership
rep = context.content

modusers=[]
users = mtool.listMemberIds()
for user in users:
    member = mtool.getMemberById(user)
    if not 'Publisher' in member.getRoles():
        for r in ['maintainer','author','licensor']:
            if rep.getContentByRole(r,user):
                modusers.append(user)
                break

return modusers
