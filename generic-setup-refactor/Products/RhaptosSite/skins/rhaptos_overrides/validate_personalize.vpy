## Controller Python Script "validate_personalize"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=email='', firstname='', surname='', fullname=''
##title=validates user preferences

## Rhaptos note: check for firstname and surname
##    make success message right
##    don't add PSM error message if we already have one, 'cause it'll double up (a Plone bug)

from Products.CMFPlone import PloneMessageFactory as _
from Products.RhaptosSite import RhaptosMessageFactory as r_

alreadyErrors = state.getErrors()

def missing(field):
    state.setError(field, r_('message_input_required', u'Input is required but no input given.'))

firstname = firstname.strip()
surname = surname.strip()
fullname = fullname.strip()

context.REQUEST.set('firstname',firstname)
context.REQUEST.set('surname',surname)
context.REQUEST.set('fullname',fullname)

if not firstname.strip():
    missing('firstname')
if not surname.strip():
    missing('surname')
if not fullname.strip():
    missing('fullname')

if state.getErrors():
    if not alreadyErrors: context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')
return state