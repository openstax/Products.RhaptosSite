## Controlled Python Script "validate_emailaddr"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=email=''
##title=Validates an email
##

## Rhaptos note: don't add PSM error message if we already have one, 'cause it'll double up (a Plone bug)

from Products.CMFPlone import PloneMessageFactory as _
reg_tool=context.portal_registration

alreadyErrors = state.getErrors()

email = email.strip()
context.REQUEST.set('email',email)

def invalid(field):
    state.setError(field, _(u'You entered an invalid email address.'), 'invalid_email')

if email and reg_tool.isValidEmail(email):
    pass
else:
    invalid('email')

if state.getErrors():
    if not alreadyErrors: context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')
else:
    return state

