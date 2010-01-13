## Script (Python) "validate_registration"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##bind state=state
##parameters=username=''
##title=Validate password setting in registration

## Rhaptos note: no counterpart in Plone.
##   no longer check for password due to PWRT

from Products.CMFPlone import PloneMessageFactory as _
from Products.RhaptosSite import RhaptosMessageFactory as r_

reg_tool=context.portal_registration

alreadyErrors = state.getErrors()

def missing(field):
    errormsg = context.translate("message_input_required", domain="rhaptos", default="Input is required but no input given.")
    state.setError(field, errormsg)
    
if not username:
    missing('username')

if not state.getError('username') and not reg_tool.isMemberIdAllowed(username):
    errormsg = context.translate("message_member_id_invalid", domain="rhaptos", default="This member id is invalid or already in use. Please choose another.")
    state.setError('username', errormsg)
  
if not state.getError('username') and len(username) < 3:
    errormsg = context.translate("message_userid_too_short", domain="rhaptos", default="Usernames must be at least 3 characters.")
    state.setError('username', errormsg)

if state.getErrors():
    if not alreadyErrors: context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')
else:
    return state
