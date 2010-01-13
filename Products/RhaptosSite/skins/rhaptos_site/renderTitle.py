## Script (Python) "renderTitle"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=page_title='', override=None
##title=Register a User
##

## Rhaptos note: no difference in conversion. no plone counterpart.
##  added course lookup

# returns correct page title
portal_title = unicode(context.portal_properties.title())
title = portal_title

if override:
    context_title = override
elif hasattr(context, 'nearestCourse'):
    context_title = context.nearestCourse().Title()
elif context.plone_utils.pretty_title_or_id(context):
    context_title = context.plone_utils.pretty_title_or_id(context)

if not same_type(u'',context_title):
    context_title = context_title.decode('utf-8')

if context_title and context_title != portal_title:
    title = title + " - " + context_title

if not override and page_title and page_title != context_title and page_title not in ["View Document", "View NewsItem"]:
    title = title + " - " + page_title

return title
