# -*- coding: utf-8 -*-
import json
import requests

# Get all Item IDs that make up crafting.
with open('woodcutting-edits.json') as json_file:
    woodcutting_data = json.load(json_file)
    
url = 'https://www.osrsbox.com/osrsbox-db/items-summary.json'
response = requests.get(url)
if(response.status_code == 200):
    all_item_data = response.json()

item_id = '1513'
item_name = all_item_data[item_id]['name']
members = False

method_name = 'woodcutting'

skills = [
    {
        'name': 'woodcutting',
        'lvl': 75,
        'xp': 250
    }
]

materials = [
#    {
#        'id': '70',
#        'quantity': 1
#    },{
#        'id': '1777',
#        'quantity': 1
#    }
]

method = [{
    'name': method_name,
    'skills': skills,
    'materials': materials,
    'members': members    
}]
    
woodcutting_data[item_id] = {
    'id': item_id,
    'name': item_name,
    'methods': method
}

#fletching_data[item_id]['methods'].append(method)

# Save edits to new json file
with open('woodcutting-edits.json', 'w') as outfile:
    json.dump(woodcutting_data, outfile, indent=4)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    