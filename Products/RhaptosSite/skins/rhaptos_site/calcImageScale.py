## Script (Python) "calcImageScale"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=image, max_width=150, max_height=150
##title=
##

# calc scale in one place

wscale = image.width/150.0
hscale = image.height/150.0
scale = max(wscale,hscale)
scale = scale < 1.0 and 1.0 or scale
return scale

