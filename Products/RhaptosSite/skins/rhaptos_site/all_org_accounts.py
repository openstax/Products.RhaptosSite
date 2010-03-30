## Script (Python) "all_org_accounts"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=return list of all org accounts

from Products.CMFCore.utils import getToolByName
mcat = getToolByName(context,'member_catalog')

return mcat({'account_type':'org'})
