# DEPRECATED! Can be removed after move to Plone 2.5

"""
Rhaptos customized memberdata class

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU General
Public License Version 2 (GPL).  See LICENSE.txt for details.
"""

"""
$Id$
"""

import zLOG
import AccessControl
from Globals import InitializeClass
from Products.CatalogMemberDataTool import MemberDataTool as CatalogMemberDataTool
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces.portal_memberdata import MemberData as IMemberData
from Products.CMFPlone.MemberDataTool import MemberDataTool

DB_FIELDS = ['honorific', 'firstname', 'othername', 'surname', 'fullname', 'lineage', 'email', 'homepage', 'comment']

BaseMemberData = CatalogMemberDataTool.MemberData
class MemberData(BaseMemberData):

    security = AccessControl.ClassSecurityInfo()

    security.declarePrivate('setMemberProperties')
    def setMemberProperties(self, mapping):
        """Overridden to store a copy of certain user data fields in an SQL database"""
        # Only pass relevant fields to the database
        db_args = dict([(f, v) for (f, v) in mapping.items() if f in DB_FIELDS and self.getProperty(f) != v])
        dbtool = getToolByName(self, 'portal_moduledb')
        if dbtool and db_args:
            # We have to pass in aq_parent to be our own parent,
            # otheriwse the ZSQL method will acquire blank arguments
            # from the property sheet
            if not self.member_catalog(getUserName=self.getId()):
                zLOG.LOG("MemberData", zLOG.INFO, "INSERT memberdata for %s: %s" % (self.getId(), db_args))
                dbtool.sqlInsertMember(aq_parent=self.aq_parent, id=self.getId(), **db_args)
            else:
                zLOG.LOG("MemberData", zLOG.INFO, "UPDATE memberdata for %s: %s" % (self.getId(), db_args))
                dbtool.sqlUpdateMember(aq_parent=self.aq_parent, id=self.getId(), **db_args)

        BaseMemberData.setMemberProperties(self, mapping)

# Backwards compatibility
XUFMemberData = MemberData

# Monkeypatch CatalogMemberDataTool to use this MemberData class
CatalogMemberDataTool.MemberData = MemberData

InitializeClass(MemberData)
