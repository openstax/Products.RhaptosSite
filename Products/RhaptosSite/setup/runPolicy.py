from Products.CMFCore.utils import getToolByName
from Products.RhaptosSite.setup.RhaptosSetup import functions

def runPolicy(context):
    ##import pdb; pdb.set_trace()
    logger = context.getLogger('rhaptossite')
    if context.readDataFile('rhaptossite.txt') is None:
        logger.info('Nothing to import')
        return
    portal = context.getSite()
    # XXX Directly calling the setup functions. There is likely a better
    #     way to do this.
    for title, func in functions:
        func(context, portal)
