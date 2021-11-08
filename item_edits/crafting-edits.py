# -*- coding: utf-8 -*-
import json

# Get all Item IDs that make up crafting.
with open('items/crafting.json') as json_file:
    crafting_data = json.load(json_file)
    
crafting_edits_dict = {}
    
# Loop through each crafting item.
for item_id in crafting_data:
    
    item_edit = dict(crafting_data[item_id])
    method_edits = []
    
    for method in item_edit['method']:
        
        method_edit = {
                'name': method['name'],
                'type': method['type'],
                'skills': [method['skill']],
                'materials': method['materials'],
                'members': method['members']
                }       
    
        method_edits.append(method_edit)
        
    item_edit['method'] = method_edits
         
    crafting_edits_dict[item_id] = item_edit

# Save edits to new josn file
with open('crafting-edits.json', 'w') as outfile:
    json.dump(crafting_edits_dict, outfile, indent=4)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    