## Script (Python) "validate_module_publish"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##bind state=state
##parameters=workspace='',otherspace=''
##title=Validate module before publishing

## Rhaptos note: no counterpart in Plone.
##    using portal_status_message given as parameter
##    return 'action' and 'workspace' through state


if not workspace:
    psm = context.translate("message_please_select_workspace", domain="rhaptos", default="Please select a workspace.")
    return state.set(status='failure', portal_status_message=psm)

if workspace == '__other__':
    workspace = otherspace

return state.set(action='accept', workspace=workspace)
