"""
Rhaptos Initialization

Author: J Cameron Cooper
(C) 2006 Rice University

This software is subject to the provisions of the GNU General
Public License Version 2 (GPL).  See LICENSE.txt for details.
"""

## allow imports in restricted code

from AccessControl import allow_module, allow_class, allow_type
from AccessControl import ModuleSecurityInfo

from AccessControl.Permissions import search_zcatalog as SearchZCatalog

# needed for validate_portrait
allow_module('mimetypes')

allow_module('Products.RhaptosSite.managercatalog')
ModuleSecurityInfo('Products.RhaptosSite.managercatalog').declareProtected(SearchZCatalog, 'workspacesSearchResults')
