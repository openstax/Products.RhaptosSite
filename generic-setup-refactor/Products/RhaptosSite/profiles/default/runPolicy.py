from Products.CMFCore.utils import getToolByName

def runPolicy(context):
    mi_tool = getToolByName(context, 'portal_migration')
    setup = mi_tool._getWidget('Rhaptos Setup')
    setup.addItems(setup.available())
