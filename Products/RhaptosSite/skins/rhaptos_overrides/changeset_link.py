##parameters=id
obj = context[id]

if obj.getId() == 'index.cnxml':
    obj = obj.nearestRhaptosObject()

typeInfo = obj.getTypeInfo();
act = typeInfo.getActionById('view')
url = ''.join((obj.absolute_url(), '/', act))
return url
