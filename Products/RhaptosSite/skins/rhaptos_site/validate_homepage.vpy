## Controller Python Script "validate_homepage"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=homepage=''
##title=validates user preferences

from Products.CMFPlone import PloneMessageFactory as _
from Products.RhaptosSite import RhaptosMessageFactory as r_

alreadyErrors = state.getErrors()

if homepage:
    homepage = homepage.strip()
    if not homepage.lower().startswith('http://'):
        if homepage.find('://') == -1:
            homepage = 'http://' + homepage    
    if homepage.find('.') == -1:
        state.setError('homepage', r_('message_not_valid_url', u'This is not a valid URL'))
    context.REQUEST.set('homepage',homepage)

if state.getErrors():
    if not alreadyErrors: context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')
else:
    return state
