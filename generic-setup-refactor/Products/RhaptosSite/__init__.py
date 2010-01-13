""" 
Rhaptos Initialization

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU General
Public License Version 2 (GPL).  See LICENSE.txt for details.
"""

# We define this first so that RhaptosSetup can import it w/o recursion
product_globals = globals()

import sys
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore import utils

from Products.GenericSetup import BASE, EXTENSION
from Products.GenericSetup import profile_registry
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

import RhaptosSite

import monkeypatch
import managercatalog  # mostly to test syntax
import security

from setup import RhaptosSitePolicy

this_module = sys.modules[ __name__ ]


# we have an EPS in our skins, and must teach FSDV how to treat it
from Products.CMFCore.DirectoryView import registerFileExtension
from Products.CMFCore.FSFile import FSFile
registerFileExtension('eps', FSFile)

from Products.PluggableAuthService import registerMultiPlugin
from Products.PluggableAuthService.permissions import ManageUsers
import pas.AltHashAuth as AHA
from AccessControl import allow_module

registerMultiPlugin(AHA.AltHashAuth.meta_type)

# Make the skins available as DirectoryViews
registerDirectory('skins', globals())

def initialize(context):
    RhaptosSitePolicy.register(context, product_globals)
    RhaptosSite.register(context, product_globals)
    
    profile_registry.registerProfile('rhaptos-default',
                                     'RhaptosSite',
                                     'Extension profile for a RhaptosSite',
                                     'profiles/default',
                                     'RhaptosSite',
                                     EXTENSION,
                                     for_=IPloneSiteRoot)

    context.registerClass( AHA.AltHashAuth
                         , permission=ManageUsers
                         , constructors=(
                            AHA.manage_addAltHashAuthForm,
                            AHA.addAltHashAuth, )
                         , visibility=None
                         , icon='pas/www/altauth.png'
                         )

# Import "RhaptosMessageFactory as _" to create message ids in the rhaptos domain
# Zope 3.1-style messagefactory module
# BBB: Zope 2.8 / Zope X3.0

allow_module('Products.RhaptosSite.messagefactory_')
try:
    from zope.i18nmessageid import MessageFactory
except ImportError:
    from messagefactory_ import RhaptosMessageFactory
else:
    RhaptosMessageFactory = MessageFactory('rhaptos')

