## Script (Python) "getMemberById"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id
##title=Proxied getMemberById so Members can see other members' name and email
## 

member = context.portal_membership.getMemberById(str(id))

if not member:
    member = context.portal_moduledb.sqlGetAuthorById(personid=str(id))
    if len(member):
        member = member[0]
    else:
        member = None
return member
