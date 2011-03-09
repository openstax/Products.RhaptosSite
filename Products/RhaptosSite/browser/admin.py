# -*- coding: utf-8 -*-
from Products.CMFPlone.browser.admin import AddPloneSite


class AddRhaptosSite(AddPloneSite):
    """Browser view used to add a Rhaptos Site similiar to how a Plone 4.x
    site is added."""

    default_extension_profiles = (
        'Products.RhaptosSite:default',
        )

    def __call__(self):
        temp_id = 'DB_OPTS_TEMP'
        form = self.request.form
        submitted = form.get('form.submitted', False)
        if submitted:
            #: Assign the DB variables to a temporary root level object
            if not hasattr(self.context,temp_id):
                self.context.manage_addFolder(temp_id)
            root = self.context[temp_id]
            root._dbopts = {}
            root._dbopts['admin'] =  form.get('dbauser', '')
            root._dbopts['adminpass'] = form.get('dbapass', '')
            root._dbopts['user'] = form.get('dbuser', '')
            root._dbopts['userpass'] = form.get('dbpass', '')
            root._dbopts['dbname'] = form.get('dbname', '')
            root._dbopts['server'] = form.get('dbserver', '')
            root._dbopts['port'] = form.get('dbport', '')
        return super(AddRhaptosSite, self).__call__()
