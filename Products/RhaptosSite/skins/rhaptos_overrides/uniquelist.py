## Script (Python) "uniquelist"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=l
##title=Reduce a list to its unique elements
##

# takes only lists of hashable objects (no lists, for example)
# this could easily be done with a 'set()' were it allowed

dict = {}
for x in l:
    dict[x] = None
return dict.keys()