## Script (Python) "hrstate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Human-readable content state

## Rhaptos note: no difference in conversion. no plone counterpart.

# Rhaptos content object must be the context
trans = {"checkedout":"Checked&nbsp;Out",
         "modified":"Modified",
         "published":"Published",
         "created":"Created",
         }
try:
    retval = trans[context.state]
except KeyError:
    # unrecognized state
    retval = context.state
except AttributeError:
    # no state available
    retval = ''
return retval
