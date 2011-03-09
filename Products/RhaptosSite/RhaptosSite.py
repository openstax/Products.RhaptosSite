# -*- coding: utf-8 -*-
from AccessControl.Permissions import view_management_screens


def zmi_constructor(context):
    """This is a dummy constructor for the ZMI."""
    url = context.DestinationURL()
    request = context.REQUEST
    return request.response.redirect(url + '/@@rhaptos-addsite?site_id=Rhaptos')


def register(context, globals):
    context.registerClass(meta_type='Rhaptos Site',
                          permission=view_management_screens,
                          constructors=(zmi_constructor,))
