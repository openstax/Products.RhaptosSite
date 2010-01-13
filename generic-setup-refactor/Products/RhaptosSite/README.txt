RhaptosSite 

  This Zope Product is part of the Rhaptos system
  (http://software.cnx.rice.edu)

  RhaptosSite provides a site setup policy for the Rhaptos system,
  pulling together and customizing the various required Products.

  To create a Rhaptos portal site, add a Plone site through the Zope
  Management Interface (ZMI) and select 'Rhaptos Site' from the
  'Customization policy setup' dropdown menu.

  This Product also contains

    - A custom MembershipTool that allows you to set the portal type
      of the folder created for members' folders.  Rhaptos defaults
      this to Workspace, a custom type based on Folder.

      It also customizes member search to use member_catalog from
      CatalogMemberDataTool (or CMFMember) and AdvancedQuery

  Creates a new portal property 'techsupport_email_address' for an email
  to send technical warnings to. On install is set to 'email_from_name'
  but may be changed.

  Requirements:

    - AdvancedQuery
    - Archetypes 1.3.X (you must replace the version of Archetypes that comes with Plone with this one)
    - CatalogMemberDataTool
    - CMFDiffTool
    - CNXMLDocument
    - CNXMLTransforms
    - CVSTool
    - FSImportTool
    - GroupUserFolder 2.0.2 (you must replace the version of GroupUserFolder that comes with Plone with this one)
    - LinkMapTool
    - ManagableIndex (>= 0.12)
    - OFolder
    - PasswordResetTool 0.3
    - Plone 2.0.X
    - References (>= 0.08)
    - RhaptosCollaborationTool
    - RhaptosCollection
    - RhaptosContent
    - RhaptosHitCountTool
    - RhaptosModuleEditor
    - RhaptosModuleStorage
    - RhaptosPatchTool
    - RhaptosPDFLatexTool
    - RhaptosRepository
    - RhaptosSimilarityTool
    - RhaptosWorkgroup
    - ZPsycopgDA

  The 'mycnx' folder should not be cached. We attempt to change the default cache rule from Cache-Fu that
  would catch it, but if you have a significantly different setup you must handle this yourself.