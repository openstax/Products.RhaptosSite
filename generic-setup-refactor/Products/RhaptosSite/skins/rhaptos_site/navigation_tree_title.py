## Script (Python) "navigation_tree_title"
##title=Render titles for navtree
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=title, charset, croppingLength
title=context.translate(title, domain="rhaptos")
if len(title) > croppingLength:
    title = (unicode(title, charset)[:croppingLength] + u'\u2026').encode(charset)
else:
    title = unicode(title, charset).encode(charset)
return ' '.join(title.split(' '))
    
