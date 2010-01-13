## Rhaptos note: no difference in conversion. no plone counterpart.

if context.REQUEST.has_key('remove'):
  ids = context.REQUEST.get('ids', None)
  if not ids:
    psm = context.translate("message_nothing_selected", domain="rhaptos", default="Nothing selected")
    return context.REQUEST.RESPONSE.redirect('collaborations?portal_status_message='+psm)

  for id in ids:
    obj = context.portal_collaboration.catalog.getobject(int(id))
    if obj.status == 'pending':
      obj.aq_parent.reverseCollaborationRequest(obj.getId())
    obj.aq_parent.manage_delObjects([obj.getId()])

  psm = context.translate("message_requests_removed", domain="rhaptos", default="Requests Removed")
  return context.REQUEST.RESPONSE.redirect('collaborations?portal_status_message='+psm)
