## Script (Python) "cc_license_accept"
##title=Make factory object when license is accepted if needed (assuming use of factory tool)
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id=None, license='', type_name=None

# pass type_name and this will create a factory object of the appropriate type for use
# by the next form.
# some borrowing from createObject script

if type_name:
    if id is None:
        id=context.generateUniqueId(type_name)

    defaultcontext = context.portal_membership.getHomeFolder()  # we have to have permissions
    new_context = defaultcontext.restrictedTraverse('portal_factory/' + type_name + '/' + id)
    return state.set(context=new_context)

return state
