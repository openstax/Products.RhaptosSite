## Controller Python Script "join_form_validate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=firstname='', surname='', email='', account_type='person', shortname='', fullname='', username='', licenseagree='', **kw
##title=validates the Registration of a User

## Rhaptos note: check for firstname and surname existence
##   don't validate password, username
##   do not say that registration has occurred
##   Also, use the rhaptos translation for the no input case
##   handles org accounts as well, since 'registration' is used for both

return state.set(status='failure')
