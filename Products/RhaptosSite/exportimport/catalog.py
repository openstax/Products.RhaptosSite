from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import IBody
from zope.component import queryMultiAdapter

filename = 'config-pendingcatalog.xml'

def importCatalog(context):
    portal = context.getSite()
    body = context.readDataFile(filename)
    if body is None:
        logger = context.getLogger('config-pendingcatalog')
        logger.info('Nothing to import')
        return
    importer = queryMultiAdapter((portal.pending_catalog, context), IBody)
    if importer:
        importer.name = 'config-pendingcatalog'
        importer.filename = filename
        importer.body = body


def exportCatalog(context):
    portal = context.getSite()
    if 'pending_catalog' not in portal.objectIds():
        logger = context.getLogger('config-pendingcatalog')
        logger.info('Nothing to export.')
        return
    exporter = queryMultiAdapter((portal.pending_catalog, context), IBody)
    if exporter:
        exporter.name = 'config-pendingcatalog'
        body = exporter.body
        if body is not None:
            context.writeDataFile(filename, body, exporter.mime_type)


def createCatalog(context):
    if context.readDataFile('rhaptossite.txt') is None:
        return
    logger = context.getLogger('create-pendingcatalog')
    portal = context.getSite()
    if 'pending_catalog' not in portal.objectIds():
        portal.manage_addProduct['ZCatalog'].manage_addZCatalog(
            'pending_catalog', 'Pending Content catalog')
        logger.info('Created Pending Content Catalog')
