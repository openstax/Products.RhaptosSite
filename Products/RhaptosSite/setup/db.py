
from Products.GenericSetup.utils import ImportConfiguratorBase


class DBImportConfigurator(ImportConfiguratorBase):

    def _getImportMapping(self):
        return {'dbconfig': {
            'admin':{},
            'adminpass':{},
            'user':{},
            'userpass':{},
            'dbname':{},
            'server':{},
            'port':{},},
            'admin':{'#text':{}},
            'adminpass':{'#text':{}},
            'user':{'#text':{}},
            'userpass':{'#text':{}},
            'dbname':{'#text':{}},
            'server':{'#text':{}},
            'port':{'#text':{}}}

def importDBConfig(context):
    logger = context.getLogger('rhaptossite')
    text = context.readDataFile('rhaptos-dbconfig.xml')
    if text is None:
        logger.info('Nothing to import.')
        return

    portal = context.getSite()
    encoding = context.getEncoding()
    config = DBImportConfigurator(portal, encoding)
    info = config.parseXML(text)

    temp_id = 'DB_OPTS_TEMP'
    if not hasattr(portal.aq_parent,temp_id):
        portal.aq_parent.manage_addFolder(temp_id)
    root = portal.aq_parent[temp_id]
    root._dbopts={}
    for key in ('admin', 'adminpass', 'user', 'userpass', 'dbname', 'server',
            'port'):
        root._dbopts[key] = info.get(key)[0].get('value', None)


