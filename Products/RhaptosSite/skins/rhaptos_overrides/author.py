## Script (Python) "author"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

# Override Plone's author.pt by redirecting to our member_profile.pt
request = container.REQUEST
RESPONSE =  request.RESPONSE

sub = list(traverse_subpath)

return RESPONSE.redirect('/member_profile/'+'/'.join(sub), 301)

