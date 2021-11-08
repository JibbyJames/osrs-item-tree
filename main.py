# -*- coding: utf-8 -*-

# Craftable Items Problem

# Generate first tree
# Check if leaves can grow
# > Each item "method" adds a new branches
# Add new tree to list
# Repeat until tree is fully grown (no new trees)
# Node names should contain item name, quantity, and method name somehow:
# methodname_quantity_itemid
# Each tree will be a row in the table

#     0
#   1   2
#  3 4 5 6

import pandas as pd
import requests
import time
import os
import json
import re

from classes.ItemTree import TreeBuilder

from datetime import date

PATH_TO_ITEM_FILES = 'items/'
PATH_TO_OUTPUT_FILES = 'output/'

API_REQUEST_INTERVAL_SECS = 4.5
API_REQUEST_ATTEMPT_LIMIT = 5

def get_item_html_ge(id):
    url = 'http://services.runescape.com/m=itemdb_oldschool/viewitem?obj=' + str(id)
    response = requests.get(url)    
    if(response.status_code == 200):
        return response.text   
    
def get_avg(lst):
    return sum(lst) / len(lst)
    
def get_all_json_item_ids():

    json_files = os.listdir(PATH_TO_ITEM_FILES)
    
    result = []
    
    # Loop through each list of items stored in JSON
    for file in json_files:
    
        with open(PATH_TO_ITEM_FILES + file) as json_file:
            json_item_data = json.load(json_file)
        
        # Add each item id to running list
        for item_id in json_item_data:
            result.append(item_id)
            
            # Also add each material used item id
            for method in json_item_data[item_id]['methods']:
                for material in method['materials']:
                    result.append(material['id'])
                
    # Remove duplicate item ids and sort
    result = list(dict.fromkeys(result))
    result.sort()
    
    return result
        

def get_ge_data(all_item_data):
    
    ''' For each JSON in the items directory, get all items and raw materials '''
    
    # GE data will be stored daily
    today = date.today().strftime("%Y_%m_%d")
    #today = "2019_10_05"
    ge_data_filename = 'ge/ge_data_' + today + '.json'
    
    # Check if we have already fetched todays data and saved to json.
    if os.path.exists(ge_data_filename):
        print('GE data exists for today. Loading from local file.')
        with open(ge_data_filename) as ge_json_file:
            result = json.load(ge_json_file)
    
    else:
        # If not we must build new dict of GE data
        result = {}
        
        # Only fetch GE data for items relvant to the skills we have data on.
        all_item_ids = get_all_json_item_ids()
        
        # Print time estimate for data scraping.
        total_ids = len(all_item_ids)
        total_seconds = total_ids * API_REQUEST_INTERVAL_SECS
        completion_time = time.strftime('%H:%M:%S', time.gmtime(total_seconds))
        print(f'About to collect GE data for {total_ids} items.')
        print(f'Estimated time for completion: {completion_time}')
        print('---------------------------------------------')
            
        # Loop through each item id
        for index, item_id in enumerate(all_item_ids):
            
            item = all_item_data[item_id]
            item_name = item['name']
        
            print('[{}/{}] Fetching GE data for item [{}]'.format((index+1), len(all_item_ids), item_name))
               
            # Only fetch GE data for items available on GE
            if item['tradeable_on_ge'] == 1:
                                
                # GE item retrieval may fail due to API limits, but this shouldn't error
                ge_item_retrieval_success = False
                attempt = 1
                
                while not (ge_item_retrieval_success or (attempt > API_REQUEST_ATTEMPT_LIMIT)):
                
                    item_html_ge = get_item_html_ge(item_id)
                    
                    amount_traded_180 = [int(i) for i in re.findall(r'trade180\.push.*, (.*)]\)', item_html_ge)]
                    daily_price_180 = [int(i) for i in re.findall(r'average180\.push.*, (.*), ', item_html_ge)]
                    
                    if len(amount_traded_180) == 0:
                        attempt = attempt + 1
                        
                        if attempt > API_REQUEST_ATTEMPT_LIMIT:
                            raise Exception('-- Final item retreival attempt failed - Try increasing the API request time --')                            
                            
                        print(f'-- Failed to retrive item data. Waiting before attempt number: [{attempt}/{API_REQUEST_ATTEMPT_LIMIT}]')
                        time.sleep(API_REQUEST_INTERVAL_SECS * 10)
                        
                    else:
                        ge_item_retrieval_success = True                        
                        result[item_id] = {
                            'id': item_id,
                            'current': daily_price_180[-1],
                            'amount_traded_180':amount_traded_180,
                            'daily_price_180':daily_price_180      
                        }        

            else:
                result[item_id] = {
                    'id': item_id,
                    'current': item['cost'],
                    'amount_traded_180': [0],
                    'daily_price_180': [0]      
                }
        
            # Force delay between items to avoid the "You've made too many requests recently." message.
            time.sleep(API_REQUEST_INTERVAL_SECS)
        
    # Save ge_data to JSON file.    
    with open(ge_data_filename, 'w') as fp:
        json.dump(result, fp, sort_keys=True)    

    return result           

def get_nature_rune_price(ge_data):
    nature_rune_id = '561'
    return ge_data[nature_rune_id]['current']

def build_method_rows(all_trees, all_item_data, ge_data):
    
    rows = []
    
    for tree_id in all_trees:
        
        row = {}
        tree = all_trees[tree_id]
    
        # Item ID
        row['Item ID'] = tree.item_id
        
        # Item Name
        row['Item Name'] = tree.item_name
        
        # Method Visual
        row['Method'] = tree.render()
        
        # [Skill X] Level + XP
        skill_data = tree.get_skill_data()
        for skill in skill_data:
            skill_name = skill.capitalize()
            row[f'{skill_name} Level'] = skill_data[skill]['lvl']
            row[f'{skill_name} XP'] = skill_data[skill]['xp']
        
        # Members
        row['Members Only'] = tree.get_members()      
        
        # Required Materials Total Cost
        required_items = []
        required_items_ge_data = tree.get_required_items_ge_data(ge_data)
        required_items_total_cost = 0
        for item in required_items_ge_data:
            quantity = item['quantity']
            name = item['name']
            cost = item['cost']
            trade_volume = round(get_avg(item['amount_traded_180'][-30:]))
            required_items.append(f'{quantity}x {name} [{cost}gp] [{trade_volume}]')
            required_items_total_cost += cost * quantity
        row['Required Items'] = '\n'.join(required_items)
        row['Required Items Total Cost'] = required_items_total_cost
        
        # Item GE Data: Tradeable on GE
        row['Item Tradeable on GE'] = (True if all_item_data[tree.item_id]['tradeable_on_ge'] == 1 else False)  
        
        # Item GE Data: Price
        item_price = ge_data[tree.item_id]["current"]
        row['Item GE Price'] = item_price
        
        # Item GE Data: Trade Volume
        row['Item GE Avg Trading Volume'] = round(get_avg(ge_data[tree.item_id]["amount_traded_180"][-30:]))
        
        # GE Profit
        row['Item GE Profit'] = item_price - required_items_total_cost
        
        # High Alch Value
        high_alch_value = all_item_data[tree.item_id]['highalch']
        row['Item High Alch Value'] = high_alch_value
      
        # High Alch Profit
        nature_rune_price = get_nature_rune_price(ge_data)
        high_alch_profit = high_alch_value - (nature_rune_price + required_items_total_cost)
        row['Item High Alch Profit'] = high_alch_profit
        
        rows.append(row)
        
    return rows


def output_to_csv(row_data):
            
    # Use poandas to save json to csv
    output_df = pd.DataFrame(row_data)
    
    # List out order of columns for output.
    output_columns = [
        'Item ID',
        'Item Name',
        'Method',
        'Members Only',
        'Required Items',
        'Required Items Total Cost',
        'Item Tradeable on GE',
        'Item GE Price',
        'Item GE Avg Trading Volume',
        'Item GE Profit',
        'Item High Alch Value',
        'Item High Alch Profit' 
    ]
    
    # Skill columns will vary depending on primary skill data used
    all_columns = output_df.columns
    skill_columns = list(filter(lambda x: ('Level' in x) or ('XP' in x), all_columns))
    skill_columns.sort()
    output_columns[4:4] = skill_columns
    
    output_file = PATH_TO_OUTPUT_FILES + 'all_skills_' + date.today().strftime("%Y%m%d") + '.csv'
    output_df.to_csv(output_file, index=False, columns=output_columns)
    
    # TODO - Output to html table with CSS formatting and JS functions
    # output_df.to_html()
    
    
# 1 - Get an up to date list of every OSRS item
url = 'https://www.osrsbox.com/osrsbox-db/items-complete.json'
response = requests.get(url)
if(response.status_code == 200):
    all_item_data = response.json()
    print('Successfully retreived latest item data.')

# 2 - Fetch GE data for items in all skill JSON files
ge_data = get_ge_data(all_item_data)

# 3 - Gather all skill data in one dict with item id as key
all_skill_data = {}
skill_files = os.listdir(PATH_TO_ITEM_FILES)
for skill_file_name in skill_files:
    
    with open(PATH_TO_ITEM_FILES + skill_file_name) as skill_file:
        skill_data = json.load(skill_file)
        
    all_skill_data.update(skill_data)
print(f'Collected {len(all_skill_data.keys())} items from json skill files.')

# 4 - Create all item crafting trees
builder = TreeBuilder()
all_trees = builder.create_all(all_skill_data, all_item_data)
print(f'Built {len(all_trees.keys())} item crafting trees')

# 5 - Build row data containing cost/profit values for each tree
row_data = build_method_rows(all_trees, all_item_data, ge_data)
print(f'Coverted trees into cost/profit rows.')

# 6 - Output the results to a CSV
output_to_csv(row_data)
print(f'Saved to file.')







