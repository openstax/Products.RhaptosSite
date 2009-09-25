#!/usr/bin/evn python
"""
Turn all actions in a .metadata file into XML for cmfformcontroller.xml insertion.

Usage: form_controller_extract.py file.metadata

Return XML; copy and paste into your profile file.

Handles actions only at the moment; validators need manual attention.
"""
import sys

actiontemplate = """  <!-- %s -->
  <action
    object_id="%s"
    status="%s"
    context_type="%s"
    button="%s"
    action_type="%s"
    action_arg="%s"
    />"""

# Check for number of arguments
if len(sys.argv) != 2:
    print "Usage: form_controller_extract.py <metdatafile> "
    sys.exit(-1)

f = open(sys.argv[1])
lines = f.readlines()
f.close()

object_id = sys.argv[1].split('/')[-1].split('.')[0]

print "  <!-- %s... -->" % object_id

for l in lines:
    l = l.strip()
    line = l.split('=')
    if len(line)==2:
        predicate, action = line
        predicate = predicate.split('.')
        if predicate[0] == 'action':
            status = predicate[1]
            try: context_type = predicate[2]
            except IndexError: context_type = ''
            try: button = predicate[3]
            except IndexError: button = ''
            
            sep = action.index(':')
            action_type = action[:sep]
            action_arg = action[sep+1:]
            
            print actiontemplate % (l, object_id, status, context_type, button, action_type, action_arg)
            print
