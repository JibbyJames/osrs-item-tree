
# Expected Output:
#
# [1,2]
# [3,4,2]
# [1,5,6]
# [3,4,5,6]
# [1,5,7,8]
# [3,4,5,7,8]

# Items represents the "all_skills_item_data" dataset
items = {}
items["0"] = { "id": "0", "children": ["1", "2"] }
items["1"] = { "id": "1", "children": ["3", "4"] }
items["2"] = { "id": "2", "children": ["5", "6"] }
items["3"] = { "id": "3", "children": [] }
items["4"] = { "id": "4", "children": [] }
items["5"] = { "id": "5", "children": [] }
items["6"] = { "id": "6", "children": ["7", "8"] }
items["7"] = { "id": "7", "children": [] }
items["8"] = { "id": "8", "children": [] }


def get_required_items(item):

    item_sets = []
    items_required = len(item['children'])
    
    print(item)
    print('  Items Required: {}'.format(items_required))
    
    for child in item["children"]:
        if child in items:
            req_items = get_required_items(items[child])
            item_sets.append(req_items)
    
    return item_sets


def get_binary_combinations(num_of_digits):

    binary_combinations = []
    
    # Get largest number
    max_num = int(num_of_digits * "1", 2)
    
    format(14, '08b')
    
    pattern = '0{}b'.format(num_of_digits)
    
    for i in range(0, max_num + 1):
        binary_combinations.append(format(i, pattern))
    
    return binary_combinations

def get_recursive_combs(item):
    
    all_combinations = []
    
    print("-- Item {} --".format(item["id"]))
    
    get_children_length = len(item['children'])
    print("Child Length: {}".format(get_children_length))
    
    combinations = get_binary_combinations(get_children_length)
    
    print("All combinations: {}".format(combinations))
    
    # ['00', '01', '10', '11']
    for combination in combinations:
        
        valid_combination = True
        
        print("Current combination: {}".format(combination))
        
        if "1" not in combination:
            print("  0 only combination automatically added")
            all_combinations.append(str(combination))
            continue
        
        offset = 0
        active_comb = str(combination)
            
        # ['0', '0']
        for index, switch in enumerate(combination):
            
            print("  Index: {}  Switch: {}".format(index, switch))
            
            # A zero means we are not going to recursively check this item
            if switch == "0":
                continue
                
            # A one means we check for chil dren.
            if switch == "1":
                
                child_id = item["children"][index]
                print("    Current switch child: {}".format(child_id))
                
                if len(items[child_id]["children"]) > 0:
                    
                    print("    Switch child has {} children".format(len(items[child_id]["children"])))              
                    
                    print("------ About to get recursive items")
                    child_combinations = get_recursive_combs(items[child_id])
                    print("    Returned from recursive function")
                    print("------ Result from function: {}".format(child_combinations))
                    
                    for child_comb in child_combinations:
                        position = index + offset
                        print("  index: {}   offset: {}   position: {}".format(index, offset, position))
                        print("  About to add '[{}]' to active_comb {}".format(child_comb, active_comb))
                        active_comb = active_comb[:position] + "[" + child_comb + "]" + active_comb[position+1:]
                        offset += len(child_comb) + 1
                else:
                    
                    print("    Switch child has {} children, invalid combination".format(len(items[child_id]["children"])))              
                    
                    # If combination is 1, but child has no children, we can exit this combination
                    valid_combination = False
                    break
                
        if valid_combination:
            print("  Adding new combination '{}'".format(active_comb))
            all_combinations.append(active_comb)

        
                
    return all_combinations      


item = items["0"]

result = get_recursive_combs(item)


# ['00', '0[00[0[00]]', '[00]0', '[00][00[0[00]]']
















