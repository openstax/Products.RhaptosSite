## Script (Python) "displayState"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=state
##title=
##

## Rhaptos note: no difference in conversion. no plone counterpart.

# Nicely format object states for display
if state == 'checkedout':
    return 'Checked Out'
else:
    return state.capitalize()
