## Script (Python) "getPending"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=portal_type=''
##title=List Intersection

res = context.pending_catalog(portal_type=portal_type,sort_on='timestamp', sort_order='reverse')

pending=[]
for p in res:
    try:
        pending.append(p.getObject())
    except AttributeError:
        pass

return pending
