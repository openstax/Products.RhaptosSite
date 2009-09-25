## Controller Python Script "personalize"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=logo=None, visible_ids=None, listed=None, REQUEST=None
##title=Personalization Handler.

from Products.CMFPlone import transaction_note
#logo_id='MyPortrait'

member=context.portal_membership.getAuthenticatedMember()
member.setProperties(context.REQUEST)
member_context=context.portal_membership.getHomeFolder(member.getId())

if member_context is None:
    member_context=context.portal_url.getPortalObject()


if (logo and logo.filename):
    context.portal_membership.changeMemberPortrait(logo)

delete_logo = context.REQUEST.get('delete_logo', None)
if delete_logo:
    context.portal_membership.deletePersonalPortrait(member.getId())

tmsg='Edited personal settings for %s' % member.getUserName()
transaction_note(tmsg)

return state.set(portal_status_message='Your personal settings have been saved.')
