from Products.CMFCore.utils import getToolByName

def runPolicy(context):
    #import pdb; pdb.set_trace()
    logger = context.getLogger('rhaptossite')
    if context.readDataFile('rhaptossite.txt') is None:
        logger.info('Nothing to import')
        return
    portal = context.getSite()
    mi_tool = getToolByName(portal, 'portal_migration')
    setup = mi_tool._getWidget('Rhaptos Setup')
    setup.addItems(setup.available())
