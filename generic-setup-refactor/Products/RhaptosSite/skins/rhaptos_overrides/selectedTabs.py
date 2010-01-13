## Script (Python) "selectedTabs"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=default_tab, obj=None, portal_tabs=[]
##title=
##

## Rhaptos note:
##  check action names against path to replicate old PLone behavior, which we use for Authoring Area highlights
##  remove (in two places) the default to match Home
##    - checking action against startswith('/') disallowed
##    - passed in default action ('index_html') unused now
##  ...which normally would disable the home entirely, but our patch above adds it only for the home page

from AccessControl import Unauthorized

# we want to centralize where all tab selection is done
# for now we will start off with the top tabs, 'portal_tabs'
url_tool = context.portal_url
plone_url = url_tool()
request = context.REQUEST
valid_actions = []

url = request['URL']
path = url[len(plone_url):]

for action in portal_tabs:
    action_path = action['url'][len(plone_url):]
    if not action_path.startswith('/'):
        action_path = '/' + action_path
    if path.startswith(action_path) and not action_path=='/':  # PATCH (second expr)
        # Make a list of the action ids, along with the path length for
        # choosing the longest (most relevant) path.
        valid_actions.append((len(action_path), action['id']))

# our patch: add action names to valid actions, to replicate the old behavior,
# which we depend on for MyCNX and other tabs monkey business
    action_path = "/%s" % action['id']
    if path.startswith(action_path):
        valid_actions.append((100000, action['id']))  # high sort number for ids to take precedence
# ...end

# Sort by path length, the longest matching path wins
valid_actions.sort()
if valid_actions:
    return {'portal':valid_actions[-1][1]}

return {'portal':''}  # PATCH: no default tab
