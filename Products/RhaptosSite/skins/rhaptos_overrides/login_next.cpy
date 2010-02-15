## Controller Python Script "login_next"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Login next actions
##

## Rhaptos note: 
##   custom form controller (.metadata) change
##   custom welcome message (includes portal name)
##   return immediately on redirect so that FormController redirect doesn't swallow portal status messages
##   for logins from home and only home, we ignore REQUEST.came_from and forward to mydashboard (action.success)

from Products.CMFPlone import PloneMessageFactory as _
from DateTime import DateTime
import ZTUtils

REQUEST = context.REQUEST

try:
    context.acl_users.credentials_cookie_auth.login()
except AttributeError:
    # The cookie plugin may not be used, or the site still uses GRUF
    pass

util = context.plone_utils
membership_tool=context.portal_membership
if membership_tool.isAnonymousUser():
    REQUEST.RESPONSE.expireCookie('__ac', path='/')
    util.addPortalMessage(_(u'Login failed'))
    return state.set(status='failure')

came_from = REQUEST.get('came_from', None)

# if we weren't called from something that set 'came_from' or if HTTP_REFERER
# is the 'logged_out' page, return the default 'login_success' form
if came_from is not None:
    scheme, location, path, parameters, query, fragment = util.urlparse(came_from)
    template_id = path.split('/')[-1]
    if template_id in ['login', 'login_success', 'login_password', 'login_failed',
                       'login_form', 'logged_in', 'logged_out', 'registered',
                       'mail_password', 'mail_password_form', 'join_form',
                       'require_login', 'member_search_results']:
        came_from = ''
    # when we login from the home page, we want to go to the author_home, aka mydashboard
    bCameFromHome = ( path == '/' or path == '/index_html' )
    if bCameFromHome:
        came_from = ''
    # It is probably a good idea in general to filter out urls outside the portal.
    # An added bonus: this fixes some problems with a Zope bug that doesn't
    # properly unmangle the VirtualHostMonster stuff when setting ACTUAL_URL
    if not context.portal_url.isURLInPortal(came_from):
        came_from = ''

js_enabled = REQUEST.get('js_enabled','1') != '0'
if came_from: # and js_enabled:  # PATCH: not a good check, breaks our intended return-to
    # If javascript is not enabled, it is possible that cookies are not enabled.
    # If cookies aren't enabled, the redirect will log the user out, and confusion
    # may arise.  Redirect only if we know for sure that cookies are enabled.

    from Products.RhaptosSite import RhaptosMessageFactory as r_
    portal = context.portal_url.getPortalObject()
    util.addPortalMessage(r_("message_logged_in_welcome",
                             default=u'Welcome to ${portal_title}! You are now logged in.',
                             mapping={"portal_title":portal.Title()}))
    came_from = util.urlunparse((scheme, location, path, parameters, query, fragment))
    return REQUEST.RESPONSE.redirect(came_from)

state.set(came_from=came_from)

return state
