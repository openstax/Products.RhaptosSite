## Script (Python) "getMemberById"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id
##title=Proxied getMemberById so Members can see other members' name and email
## 

return context.portal_membership.getMemberById(str(id))
