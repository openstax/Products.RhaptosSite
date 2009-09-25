## Controller Python Script "validate_affil_url"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=affiliation_url=''
##title=validates user preferences

from Products.CMFPlone import PloneMessageFactory as _
from Products.RhaptosSite import RhaptosMessageFactory as r_

alreadyErrors = state.getErrors()

if affiliation_url:
    affiliation_url = affiliation_url.strip()
    if not affiliation_url.lower().startswith('http://'):
        if affiliation_url.find('://') == -1:
            affiliation_url = 'http://' + affiliation_url    
    if affiliation_url.find('.') == -1:
        state.setError('affiliation_url', 'This is not a valid URL')
    context.REQUEST.set('affiliation_url',affiliation_url)

if state.getErrors():
    if not alreadyErrors: context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')
else:
    return state
