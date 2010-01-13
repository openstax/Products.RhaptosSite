## Controlled Python Script "validate_license"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=license=None, agree=None
##title=Validates CNX license acceptance
##

# FIXME: This should really be in a tool somewhere
VALID_LICENSES = ['http://creativecommons.org/licenses/by/2.0/', 'http://creativecommons.org/licenses/by/3.0/']
lerr = context.translate("message_please_correct_errors", domain="rhaptos", default="Please correct the indicated errors.")

if license not in VALID_LICENSES:
  errormsg = context.translate("message_choose_valid_license", domain="rhaptos" ,default="Please choose a valid license.")
  state.setError('license', errormsg)

if not agree:
  lerr = context.translate("message_agree_to_license_to_proceed", domain="rhaptos", default="You must agree to the license to proceed.")
  errormsg = context.translate("message_check_box_to_agree", domain="rhaptos", default="Check this box if you agree to the license terms.")
  state.setError('agree', errormsg)

if state.getErrors():
    return state.set(status='failure', portal_status_message=lerr)
else:
    return state
