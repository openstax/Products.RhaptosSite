## Script (Python) "listInList"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=list1, list2
##title=List Intersection

# True iff at least one of the members of list1 is in list2
# Like saying "list1[0] in list2 or list1[1] in list2 or ... or list1[n] in list2"
# You don't want to pass in very large lists.

#return bool(set(list1).intersection(set(list2)))   # ...would be nice

for elt in list1:
    if elt in list2:
        return True
return False