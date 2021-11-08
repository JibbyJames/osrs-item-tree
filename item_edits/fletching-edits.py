# -*- coding: utf-8 -*-
import json
import requests

# Get all Item IDs that make up crafting.
with open('fletching-edits.json') as json_file:
    fletching_data = json.load(json_file)
    
url = 'https://www.osrsbox.com/osrsbox-db/items-summary.json'
response = requests.get(url)
if(response.status_code == 200):
    all_item_data = response.json()

item_id = '859'
item_name = all_item_data[item_id]['name']
members = True

method_name = 'fletching-strung-bows'

skills = [
    {
        'name': 'fletching',
        'lvl': 85,
        'xp': 91.5
    }
]

materials = [
    {
        'id': '70',
        'quantity': 1
    },{
        'id': '1777',
        'quantity': 1
    }
]

method = [{
    'name': method_name,
    'skills': skills,
    'materials': materials,
    'members': members    
}]
    
fletching_data[item_id] = {
    'id': item_id,
    'name': item_name,
    'methods': method
}

#fletching_data[item_id]['methods'].append(method)

# Save edits to new json file
with open('fletching-edits.json', 'w') as outfile:
    json.dump(fletching_data, outfile, indent=4)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    