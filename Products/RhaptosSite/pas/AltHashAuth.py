"""
PAS plugin for authenticating agains a standard ZODB User Manager plugin
that has a non-standard password hash. Specifically, 'crypt', though it
could be extended.

Author: J. Cameron Cooper
Copyright (c) 2007, Rice University. All Rights Reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
import crypt

from zope.interface import Interface

from AccessControl import ClassSecurityInfo, AuthEncoding
from AccessControl.SecurityManagement import getSecurityManager

from OFS.Cache import Cacheable
from App.class_init import default__class_init__ as InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.permissions import ManageUsers
from Products.PluggableAuthService.utils import classImplements

manage_addAltHashAuthForm = PageTemplateFile(
    'www/addAltAuth', globals(), __name__='manage_addAltHashAuthForm' )

def addAltHashAuth( dispatcher, id, title=None, REQUEST=None ):
    """ Add a AltHashAuthn to a Pluggable Auth Service. """

    o = AltHashAuth(id, title)
    dispatcher._setObject(o.getId(), o)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'AltHashAuth+added.'
                            % dispatcher.absolute_url())

class IAltHashAuth(Interface):
    """ Marker interface.
    """
    
class AltHashAuth(BasePlugin, Cacheable):

    """ PAS plugin for authenticating users with an alternate hash scheme against a
    standard PAS ZODB user folder.
    """
    
    meta_type = 'Alternative Hash Authentication for ZODB User Manager'

    target_id = ""
    _properties = ( { 'id'    : 'title'
                    , 'label' : 'Title'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  , { 'id'    : 'target_id'
                    , 'label' : 'Target Plugin Id'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  )
    security = ClassSecurityInfo()

    def __init__(self, id, title=None):

        self._id = self.id = id
        self.title = title
        self.target_id = "source_users"
    
    #
    #   IAuthenticationPlugin implementation
    #
    security.declarePrivate( 'authenticateCredentials' )
    def authenticateCredentials(self, credentials):
        """ See IAuthenticationPlugin.
        
        Basically this is like the same method from ZODBUserManager except that we preprocess
        the password before digesting is, since the migration hashed an already-hashed value.
        
        Oh, and we look up the proper plugin by id provided by property.

        o We expect the credentials to be those returned by
          ILoginPasswordExtractionPlugin.
        """
        login = credentials.get( 'login' )
        password = credentials.get( 'password' )
        
        if login is None or password is None:
            return None

        targetname = self.target_id
        target = getattr(self, targetname)
        
        userid = target._login_to_userid.get(login, login)
        reference = target._user_passwords.get(userid)
        if reference is None: return None
        
        salt = userid[:2]
        hashed = crypt.crypt(password, salt)

        if AuthEncoding.pw_validate(reference, hashed):  # it would normally be reference, password here
            return userid, login
        
        return None
    
classImplements(AltHashAuth,
                IAuthenticationPlugin,
                IAltHashAuth,
               )

InitializeClass(AltHashAuth)
