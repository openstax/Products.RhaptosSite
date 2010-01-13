## Script (Python) "suggestUserNames"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Come up with a list of suggested names

email = context.REQUEST.get('email', '')
firstname = context.REQUEST.get('firstname', '')
#othername = context.REQUEST.get('othername', '')
surname = context.REQUEST.get('surname', '')

suggestions = []
if email:
    emailboth = email.split('@')
    if len(emailboth) == 2:   # email suggestions only work if valid
        emailname = emailboth[0]
        emailboth[1] = emailboth[1].split('.')[0]
        emailboth = '_'.join(emailboth)
        suggestions = suggestions + [emailname, emailboth]
if surname:
    lastnameattempt = surname.lower()
    suggestions = suggestions + [lastnameattempt]
    if firstname:
        firstinitialattempt = firstname[0].lower() + surname.lower()
        fullnameattempt = firstname + '_' + surname
        #twoinitialattempt = (firstname[0] + othername[0:1] + surname).lower()
        suggestions = suggestions + [firstinitialattempt, fullnameattempt]

# Make sure there are no duplicates while preserving order
suggestionset = []   # if only we could use a real set here. sigh.
for s in suggestions:
    if s not in suggestionset:
        suggestionset.append(s)

# Now filter out names that aren't available
reg_tool=context.portal_registration
available = []
unavailable = []
for name in suggestionset:
    if reg_tool.isMemberIdAllowed(name):
        available.append(name)
    else:
        unavailable.append(name)

return (available, unavailable)

