## Script (Python) "validate_module_publish"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##bind state=state
##parameters=message=''
##title=Validate module before publishing

## Rhaptos note: no counterpart in Plone.
##    using portal_status_message given as parameter

if not message:
    errormsg = context.translate("message_this_field_required", domain="rhaptos", default="This field is required.")
    state.setError('message', errormsg)

if state.getErrors():
    psm = context.translate("message_please_correct_errors", domain="rhaptos", default="Please correct the indicated errors.")
    return state.set(status='failure', portal_status_message=psm)
else:
    return state
