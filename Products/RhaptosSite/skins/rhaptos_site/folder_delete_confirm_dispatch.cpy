## Controlled Python Script "validate_license"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=paths=None
##title=Validates that there are items to delete
##
from Products.CMFPlone import PloneMessageFactory as _

if not paths:
  message=_(u'Please select one or more items to delete.')
  state.setError('paths', message)

if state.getErrors():
    return state.set(status='failure', portal_status_message=message)
else:
    return state
