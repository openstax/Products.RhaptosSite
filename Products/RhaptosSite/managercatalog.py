"""
Access to ZCatalog (mostly portal_catalog) that is safe for Managers.

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2009 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
from Products.CMFCore.utils import _getAuthenticatedUser

def workspacesSearchResults(catalog, REQUEST=None, **kw):
    """Catalog search rseults, but only for those objects for which you have a specific ownership.
    That is, we take the roles out of allowedRolesAndUsers.
    This can still bite a few users (whomever owns the portal) but most managers will
    get a reasonable set of data--only what they own.
    Unlike regular searchResults, doesn't check for expiry, since we don't use that.
    """
    user = _getAuthenticatedUser(catalog)
    allowedRolesAndUsers = catalog._listAllowedRolesAndUsers(user)
    allowedRolesAndUsers = [x for x in allowedRolesAndUsers if x.startswith('user:')]
    kw['allowedRolesAndUsers'] = allowedRolesAndUsers
    return catalog.unrestrictedSearchResults(REQUEST, **kw)
