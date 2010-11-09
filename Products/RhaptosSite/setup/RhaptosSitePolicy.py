"""
Rhaptos site policy definition for customizing Plone at site-creation

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU General
Public License Version 2 (GPL).  See LICENSE.txt for details.
"""

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.CustomizationPolicy import ICustomizationPolicy
from Products.CMFPlone.CustomizationPolicy import DefaultCustomizationPolicy
from Products.RhaptosSite.RhaptosSite import RhaptosGenerator

class RhaptosSitePolicy(DefaultCustomizationPolicy):
    """Customizes a fresh Plone site """
    implements(ICustomizationPolicy)

    availableAtConstruction=1

    def getPloneGenerator(self):
        return RhaptosGenerator()

    def customize(self, portal):
        DefaultCustomizationPolicy.customize(self, portal)
        
        mi_tool = getToolByName(portal, 'portal_migration')
        setup = mi_tool._getWidget('Rhaptos Setup')
        setup.addItems(setup.available())

# XXX: refactor
#def register(context, app_state):
#    addPolicy('Rhaptos Site', RhaptosSitePolicy())
