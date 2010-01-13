##parameters=name

## Rhaptos note: no difference in conversion. no plone counterpart.

# FIXME: This is really a bad, non-portable way of doing this.  We'd
# really like to do:
# context.portal_membership.searchForMembers(name=name) but it's just
# too slow.  Maybe if we optimize our memberdata tool so it doesn't
# hit the DB every time...
return name.lower() in [n.lower() for n in context.Members.objectIds()]
