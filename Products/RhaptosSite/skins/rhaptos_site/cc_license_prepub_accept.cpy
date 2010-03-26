## Script (Python) "cc_license_prepub_accept"
##title=update the licence property and restart publish workflow.
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id=None, license='', type_name=None

# parameter license has the new license value

#context.plone_log('setting the license to: %s' % license)

request = context.REQUEST

context.manage_changeProperties({'license': license})

return state.set(status='success', next_action='traverse_to_action:string:publish')
