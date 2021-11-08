# -*- coding: utf-8 -*-
import json

# Get all Item IDs that make up enchanting.
with open('items/enchanting.json') as json_file:
    enchanting_data = json.load(json_file)
    
enchanting_edits_dict = {}
    
# Loop through each enchanting item.
for item_id in enchanting_data:
    
    item = enchanting_data[item_id]
        
    item_edit = {
            'id': item['id'],
            'name':item['name']
            }
    
    new_methods = []
    
    for method in item['method']:
        
        skills = [{
                'name': 'magic',
                'lvl': item['level'],
                'xp': item['xp']            
                }]
        
        new_method = {
                'name': method['name'],
                'type': method['type'],
                'skills': skills,
                'materials': method['materials'],
                'members': item['members']
                }
        
        new_methods.append(new_method)
        
    item_edit['method'] = new_methods
         
    enchanting_edits_dict[item_id] = item_edit

# Save edits to new josn file
with open('enchanting-edits.json', 'w') as outfile:
    json.dump(enchanting_edits_dict, outfile, indent=4)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    