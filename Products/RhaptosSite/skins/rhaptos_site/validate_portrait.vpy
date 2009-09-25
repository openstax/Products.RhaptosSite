## Controller Python Script "validate_portrait"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=delete_portrait=False,portrait=None
##title=Validates portrait on prefs
##
import mimetypes

from Products.CMFPlone import PloneMessageFactory as _
from Products.RhaptosSite import RhaptosMessageFactory as r_

alreadyErrors = state.getErrors()

size = 0
id_from_file = 0

if not(delete_portrait):
    if portrait is None:
        filename=None
    else:
        filename=getattr(portrait, 'filename', None)

    if hasattr(context, 'get_size'):  # make sure things work with portal_factory
        size=context.get_size()

    if filename:
        typ, encoding = mimetypes.guess_type(filename,False)
        if not typ:
            errormsg = context.translate("message_file_doesnt_exist",{"filename":filename}, domain="rhaptos", default='File "%s" apparently does not exist' %filename)
            state.setError('portrait', errormsg)
	else:
            if not(typ.startswith('image')):
                errormsg = context.translate("message_file_not_image",{"filename":filename}, domain="rhaptos", default='Portrait file "%s" apparently not an image' %filename)
                state.setError('portrait', errormsg)

if state.getErrors():
    if not alreadyErrors: context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')
else:
    return state
