# -*- coding: utf-8 -*-
import json
import requests

# Get all Item IDs that make up crafting.
with open('smithing-edits.json') as json_file:
    smithing_data = json.load(json_file)
    

    
#    "1759": {
#        "id": "1759",
#        "name": "Ball of wool",
#        "method": [
#            {
#                "name": "spinning",
#                "type": "spinning",
#                "skills": [
#                    {
#                        "name": "crafting",
#                        "lvl": 1,
#                        "xp": 2.5
#                    }
#                ],
#                "materials": [
#                    {
#                        "id": "1737",
#                        "quantity": 1
#                    }
#                ],
#                "members": false
#            }
#        ]
#    },

url = 'https://www.osrsbox.com/osrsbox-db/items-summary.json'
response = requests.get(url)
if(response.status_code == 200):
    all_item_data = response.json()
    
# Bronze Bar: 2349
# Blurite: 9467
# Iron: 2351
# Silver: 2355
# Steel: 2353
# Mithril: 2359
# Adamite: 2361
# Runite: 2363


item_id = '1127'
item_name = all_item_data[item_id]['name']
members = False

method_type = 'anvil-smithing'
method_name = 'rune-anvil-smithing'

skills = [
    {
        'name': 'smithing',
        'lvl': 99,
        'xp': 375	
    }
]

materials = [
    {
        'id': '2363',
        'quantity': 5
    }
#    ,{
#        'id': '1513',
#        'quantity': 1
#    }         
]

method = [{
    'name': method_name,
    'type': method_type,
    'skills': skills,
    'materials': materials,
    'members': members    
}]
    
smithing_data[item_id] = {
    'id': item_id,
    'name': item_name,
    'methods': method
}

# Save edits to new json file
with open('smithing-edits.json', 'w') as outfile:
    json.dump(smithing_data, outfile, indent=4)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    