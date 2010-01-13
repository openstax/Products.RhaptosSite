## Controller Python Script "logged_in"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Initial post-login actions
##

## Rhaptos note: make non-Members unable to log in (requires 'member' defn moved up)
## Plone 2.5 note: previously changed initial password and came_from behaviors here, but no longer available
##   Also set the user's status to 'Approved' at login

from Products.CMFPlone import PloneMessageFactory as _
from Products.RhaptosSite import RhaptosMessageFactory as r_
REQUEST=context.REQUEST

# If someone has something on their clipboard, expire it.
if REQUEST.get('__cp', None) is not None:
    REQUEST.RESPONSE.expireCookie('__cp', path='/')

membership_tool=context.portal_membership
member = membership_tool.getAuthenticatedMember()
roles = member.getRoles()
if membership_tool.isAnonymousUser() or 'Member' not in roles and 'Manager' not in roles: # Rhaptos: second clause
    REQUEST.RESPONSE.expireCookie('__ac', path='/')
    context.plone_utils.addPortalMessage(_(u'Login failed'))
    return state.set(status='failure')

login_time = member.getProperty('login_time', '2000/01/01')
initial_login = int(str(login_time) == '2000/01/01')
state.set(initial_login=initial_login)

member.setProperties({'status':'Approved'})

must_change_password = member.getProperty('must_change_password', 0)
state.set(must_change_password=must_change_password)

if initial_login:
    state.set(status='initial_login')
elif must_change_password:
    state.set(status='change_password')

membership_tool.setLoginTimes()
membership_tool.createMemberArea()

return state
