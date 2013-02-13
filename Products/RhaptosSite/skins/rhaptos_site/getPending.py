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
for r in res:
    try:
        p = r.getObject())
        if p.state == 'pending':
            pending.append(p)
    except AttributeError:
        continue

return pending
