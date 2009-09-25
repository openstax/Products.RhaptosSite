## Controller Python Script "register"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=password='password', password_confirm='password_confirm', came_from_prefs=None
##title=Register a User
##

## Rhaptos note:
##  run a strip on incoming user name
##  create fullname here
##     (Plone has a field, previously we created it in a hidden field
##      in confirm_account_form, now deleted.)

from Products.CMFPlone import PloneMessageFactory as _
from ZODB.POSException import ConflictError

REQUEST = context.REQUEST

portal_registration = context.portal_registration
site_properties = context.portal_properties.site_properties

username = REQUEST['username'].strip()
password=REQUEST.get('password') or portal_registration.generatePassword()
if not REQUEST.get('fullname'):
    REQUEST.set('fullname', "%s %s" % (REQUEST.get('firstname'), REQUEST.get('surname')))
# This is a temporary work-around for an issue with CMF not properly
# reserving some existing ids (FSDV skin elements, for example). Until
# this is fixed in the CMF we can at least fail nicely. See
# http://dev.plone.org/plone/ticket/2982 and http://plone.org/collector/3028
# for more info. (rohrer 2004-10-24)
try:
    portal_registration.addMember(username, password, properties=REQUEST)
except AttributeError:
    state.setError('username', _(u'The login name you selected is already in use or is not valid. Please choose another.'))
    context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')

account_type = REQUEST.get('account_type','')
if account_type == 'org':
	roles = ('Member','Endorser')
else:
	roles = ('Member',)
context.acl_users.userFolderEditUser(username,None,roles)

if site_properties.validate_email or REQUEST.get('mail_me', 0):
    try:
        portal_registration.registeredNotify(username)
    except ConflictError:
        raise
    except Exception, err:

        # TODO registerdNotify calls into various levels.  Lets catch all
        # exceptions.  Should not fail.  They cant CHANGE their password ;-)
        # We should notify them.
        #
        # (MSL 12/28/03) We also need to delete the just made member and return to the join_form.
        msg = _(u'We were unable to send your password to your email address: ${address}',
                mapping={u'address' : str(err)})
        state.setError('email', msg)
        state.set(came_from='login_success')
        context.acl_users.userFolderDelUsers([username,])
        context.plone_utils.addPortalMessage(_(u'Please enter a valid email address.'))
        return state.set(status='failure')

state.set(came_from=REQUEST.get('came_from','login_success'))

if came_from_prefs:
    context.plone_utils.addPortalMessage(_(u'User added.'))
    state.set(status='prefs')

from Products.CMFPlone import transaction_note
transaction_note('%s registered' % username)

return state
