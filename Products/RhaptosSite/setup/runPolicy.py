from Products.CMFCore.utils import getToolByName

def runPolicy(context):
    #import pdb; pdb.set_trace()
    mi_tool = getToolByName(context._site, 'portal_migration')
    setup = mi_tool._getWidget('Rhaptos Setup')
    setup.addItems(setup.available())
