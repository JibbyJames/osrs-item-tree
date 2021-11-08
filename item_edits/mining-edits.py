# -*- coding: utf-8 -*-
import json
import requests

# Get all Item IDs that make up crafting.
with open('mining-edits.json') as json_file:
    mining_data = json.load(json_file)

url = 'https://www.osrsbox.com/osrsbox-db/items-summary.json'
response = requests.get(url)
if(response.status_code == 200):
    all_item_data = response.json()

item_id = '451'
item_name = all_item_data[item_id]['name']
members = False

method_name = 'mining'

skills = [
    {
        'name': 'mining',
        'lvl': 85,
        'xp': 125
    }
]

materials = []

method = [{
    'name': method_name,
    'skills': skills,
    'materials': materials,
    'members': members    
}]
    
mining_data[item_id] = {
    'id': item_id,
    'name': item_name,
    'methods': method
}

# Save edits to new json file
with open('mining-edits.json', 'w') as outfile:
    json.dump(mining_data, outfile, indent=4)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    