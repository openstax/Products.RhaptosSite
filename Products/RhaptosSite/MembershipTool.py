# DEPRECATED! Can be removed after move to Plone 2.5

"""
Rhaptos customized membership tool

Author: Brent Hendricks, Cameron Cooper
(C) 2005 Rice University

This software is subject to the provisions of the GNU General
Public License Version 2 (GPL).  See LICENSE.txt for details.
"""

import shlex
import zLOG
from Globals import InitializeClass
from Acquisition import aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName, _checkPermission
from Products.CMFPlone.MembershipTool import MembershipTool as BaseTool
from Products.AdvancedQuery import Eq, MatchGlob, Or, And

class MembershipTool( BaseTool ):
    """Customized Membership Tool"""

    meta_type = 'Rhaptos Membership Tool'

    membersfolder_type = "Folder"

    # this should probably be in MemberDataTool.py
    #security.declarePublic( 'searchForMembers' )
    def searchForMembers( self, REQUEST=None, **kw ):
        """Search for users (not groups, not groups-as-users) of a site """
        if REQUEST:
            dict = REQUEST
        else:
            dict = kw

        name = dict.get('name', '')
        # Split up search terms but leave quoted ones together
        try:
            names = shlex.split(name)
        except ValueError:
            try:
                names = shlex.split(name.replace("'","\\'"))
            except ValueError:
                names = shlex.split(name.replace("'","\\'")+'"')

        # Short circuit: if all that was asked for was '*', just return everyone
        if names == ['*']:
            query = And()
        else:
            queries = []
            for name in names:
                queries.extend([MatchGlob('fullname', name), MatchGlob('email', name), Eq('getUserName', name)])
            query = Or(*queries)
        zLOG.LOG('MembershipTool', zLOG.BLATHER, 'Querying: %s' % query)

        catalog = getToolByName(self, 'member_catalog')
        return catalog.evalAdvancedQuery(query, ('surname', 'firstname'))

##     def createMemberarea(self, member_id):
##         """Create a space in the portal for the given member """
##         zLOG.LOG("RhaptosSite.MembershipTool", zLOG.INFO, "createMemberarea for user %s" % member_id)
##         parent = self.aq_inner.aq_parent
##         members = self.getMembersFolder()
##         pt = getToolByName( self, 'portal_types' )

##         if member_id and self.getMemberareaCreationFlag():
##             if members is None:
##                 # add Members folder if it doesn't exist
##                 zLOG.LOG("RhaptosSite.MembershipTool", zLOG.INFO, "need to create Members folder")
##                 parent.invokeFactory("Folder", self.getMemberareaFolderId())
##                 members = self.getHomeFolder()
##                 members.setTitle("Members")
##                 members.setDescription("Container for portal members' home folders")
##                 # how about ownership?

##                 # this stuff like MembershipTool...
##                 portal_catalog = getToolByName( self, 'portal_catalog' )
##                 portal_catalog.unindexObject(members)     # unindex Memberareas folder
##                 members._setProperty('right_slots', (), 'lines')

##             if members is not None and not hasattr(members, member_id):
##                 # add workspace to Members folder
##                 zLOG.LOG("RhaptosSite.MembershipTool", zLOG.INFO, "creating workspace for user %s" % member_id)
##                 members.invokeFactory(self.getMemberareaType(), member_id)
##                 space = self.getHomeFolder(member_id)
##                 space.setTitle("%s's Workspace" % member_id)
##                 space.setDescription("Home page area that contains the items created and " \
##                                      + "collected by %s" % member_id)

##                 # grant ownership to member
##                 acl_users = self.__getPUS()
##                 user = acl_users.getUser(member_id)
##                 if user is not None:
##                     user= user.__of__(acl_users)
##                 else:
##                     from AccessControl import getSecurityManager
##                     user= getSecurityManager().getUser()
##                     # check that we do not do something wrong
##                     if user.getUserName() != member_id:
##                         raise NotImplementedError, \
##                               'cannot get user for member area creation'
##                 space.changeOwnership(user)
##                 space.manage_setLocalRoles(member_id, ['Owner'])

##                 import transaction
##                 transaction.commit(1) #so we can have access to the full member object
##                 member_object=self.getMemberById(member_id)

##                 # Hook to allow doing other things after memberarea creation.
##                 notify_script = getattr(space, 'notifyMemberAreaCreated', None)
##                 if notify_script is not None:
##                     notify_script()

    #security.declareProtected(permissions.ManagePortal, 'setMemberProperties')
    def setMemberProperties(self, member, **properties):
        if hasattr(member, 'getId'):
            member=member.getId()
        user=self.getMemberById(member)
        user.setMemberProperties(properties)
 



InitializeClass(MembershipTool)
