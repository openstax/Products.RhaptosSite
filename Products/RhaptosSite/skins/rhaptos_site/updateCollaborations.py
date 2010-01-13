## Rhaptos note: no difference in conversion. no plone counterpart.

context.REQUEST.RESPONSE.setHeader('Content-type','text/html')
ids = context.REQUEST.get('ids', [])
if not ids:
  psm = context.translate("message_nothing_selected", domain="rhaptos", default="Nothing selected")
  return context.REQUEST.RESPONSE.redirect('collaborations?portal_status_message='+psm)

if context.REQUEST.has_key('accept'):
  if not context.REQUEST.has_key('agree'):
    psm = context.translate("message_agree_to_license_to_proceed", domain="rhaptos", default="You must agree to the license to proceed.")
    return context.REQUEST.RESPONSE.redirect('collaborations?portal_status_message='+psm)
  for id in ids:
    try:
      obj = context.portal_collaboration.catalog.getobject(int(id))
    except KeyError:
      psm = context.translate("message_warning_request_changed", domain="rhaptos", default="Warning: That request was canceled or changed.")
      return context.REQUEST.RESPONSE.redirect('collaborations?portal_status_message='+psm)
    obj.setStatus('accepted')
  psm = context.translate("message_accepted_roles", domain="rhaptos", default="Accepted roles")
  return context.REQUEST.RESPONSE.redirect('collaborations?portal_status_message='+psm)

elif context.REQUEST.has_key('reject'):
  for id in ids:
    try:
      obj = context.portal_collaboration.catalog.getobject(int(id))
    except KeyError:
      psm = context.translate("message_warning_request_changed", domain="rhaptos", default="Warning: That request was canceled or changed.")
      return context.REQUEST.RESPONSE.redirect('collaborations?portal_status_message='+psm)
    obj.setStatus('rejected')
  psm = context.translate("message_rejected_roles", domain="rhaptos", default="Rejected roles")
  return context.REQUEST.RESPONSE.redirect('collaborations?portal_status_message='+psm)

else:
  psm = context.translate("message_unknown_action", domain="rhaptos", default="Unknown action")
  return context.REQUEST.RESPONSE.redirect('collaborations?portal_status_message='+psm)
