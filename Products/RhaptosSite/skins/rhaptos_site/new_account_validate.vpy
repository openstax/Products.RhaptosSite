## Controller Python Script "new_account_validate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=firstname='', surname='', email='', account_type='person', shortname='', fullname='', username='', licenseagree='', **kw
##title=validates the Registration of a User

## Rhaptos note: check for firstname and surname existence
##   don't validate password, username
##   do not say that registration has occurred
##   Also, use the rhaptos translation for the no input case
##   handles org accounts as well, since 'registration' is used for both

from Products.CMFPlone import PloneMessageFactory as _
from Products.RhaptosSite import RhaptosMessageFactory as r_

alreadyErrors = state.getErrors()

reg_tool=context.portal_registration
def missing(field):
    state.setError(field, r_(u'Input is required but no input given.'), 'message_input_required')

email = email.strip()
context.REQUEST.set('email',email)

if not email:
    missing('email')
if not username:
    missing('username')
if not licenseagree and getattr(context,'sitelicense',None) :
    state.setError('licenseagree',
                   _(u'You must agree to the license to proceed.'),
                   'licenseagree_invalid')


if account_type == 'org':
   shortname = shortname.strip()
   fullname = fullname.strip()

   context.REQUEST.set('shortname',shortname)
   context.REQUEST.set('surname',shortname)
   context.REQUEST.set('fullname',fullname)

   if not shortname:
       missing('shortname')
   if not fullname:
       missing('fullname')
else:
   firstname = firstname.strip()
   surname = surname.strip()

   context.REQUEST.set('firstname',firstname)
   context.REQUEST.set('surname',surname)

   if not firstname:
       missing('firstname')
   if not surname:
       missing('surname')

if not state.getError('username') and not reg_tool.isMemberIdAllowed(username):
    state.setError('username',
                   _(u'The login name you selected is already in use or is not valid. Please choose another.'),
                   'username_invalid')

if state.getErrors():
    if not alreadyErrors: context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    if account_type == 'org':
        return state.set(status='org_failure')
    else:
        return state.set(status='failure')

else:
    return state
