# -*- coding: utf-8 -*-
import json
import requests

# Get all Item IDs that make up crafting.
with open('magic-edits.json') as json_file:
    magic_data = json.load(json_file)

url = 'https://www.osrsbox.com/osrsbox-db/items-summary.json'
response = requests.get(url)
if(response.status_code == 200):
    all_item_data = response.json()

item_id = '1761'
item_name = all_item_data[item_id]['name']
members = True

method_name = 'humidify-steam-battlestaff'

skills = [
    {
        'name': 'magic',
        'lvl': 68,
        'xp': 65
    }
]

materials = [{
    'id': '9075',
    'quantity': 1 / 27
}]

method = [{
    'name': method_name,
    'skills': skills,
    'materials': materials,
    'members': members    
}]
    
magic_data[item_id] = {
    'id': item_id,
    'name': item_name,
    'methods': method
}

# Save edits to new json file
with open('magic-edits.json', 'w') as outfile:
    json.dump(magic_data, outfile, indent=4)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    