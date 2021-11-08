ims = {}
ims["item_0"] = { "id": "item_0", "children": ["method_0", "method_1"] }
ims["item_1"] = { "id": "item_1", "children": ["method_2"] }
ims["item_2"] = { "id": "item_2", "children": [] }
ims["item_3"] = { "id": "item_3", "children": [] }
ims["item_4"] = { "id": "item_4", "children": [] }
ims["item_5"] = { "id": "item_5", "children": [] }
ims["method_0"] = { "id": "method_0", "children": ["item_1", "item_2"] }
ims["method_1"] = { "id": "method_1", "children": ["item_1", "item_3"] }
ims["method_2"] = { "id": "method_2", "children": ["item_4", "item_5"] }

# input output data types?
# E.g.: input[method_id] = item_0
#       output[item_id] = [method_0, method_1]
#

# Desired output for creating item_0:
# [method_0]
# [method_1]
# []
#

def get_binary_combinations(num_of_digits):

    binary_combinations = []
    
    # Get largest possible binary number of X digits
    max_num_binary = num_of_digits * "1"
    max_num = int(max_num_binary, 2)
            
    # Pattern adds leading zeros to keep digit count consistent
    pattern = '0{}b'.format(num_of_digits)
    
    # Count from 0 to max_num, representing all combinations.
    for i in range(0, max_num + 1):
        binary_combinations.append(format(i, pattern))
    
    return binary_combinations


def get_child_combinations(item_id):
    item = ims[item_id]    
    count_of_children = len(item["children"])    
    return get_binary_combinations(count_of_children)

def has_children(item):
    return("children" in item) and (len(item["children"]) > 0)

def insert_child_combination(index, string, new_string):
    result = string[:index] + "[" + new_string + "]" + string[index+1:]
    return result

def get_item_binary_combinations(item):
      
    combination_edits = []

    item_combinations = get_child_combinations(item["id"])
    
    # ['00', '01', '10', '11']
    for combination_index, combination in enumerate(item_combinations):
        
        # We build up the final combination by going through each child
        active_combinations = []
        
        # A combination of all zeros represents no recursive methods
        if "1" not in combination:
            combination_edits.append(combination)
            continue
        
        # ["0", "1"]
        switch_index_progress = 0
        for switch_index, switch in enumerate(combination):
            
            child = ims[item["children"][switch_index]]
            
            if switch == "0":
                if len(active_combinations) == 0:
                    active_combinations.append("0")
                else:
                    for ac in range(len(active_combinations)):
                        active_combinations[ac] += "0"
    
            if switch == "1":
            
                child = ims[item["children"][switch_index]]
                
                if has_children(child):                    
                    
                    child_combinations = get_item_binary_combinations(child)
                                            
                    if len(active_combinations) == 0:
                        for cc in range(len(child_combinations)):
                            active_combinations.append("[" + child_combinations[cc] + "]")
                    else:                        
                        new_active_combinations = []
                        
                        for ac in active_combinations:
                            for cc in child_combinations:
                                new_comb = "{}[{}]".format(ac, cc)
                                new_active_combinations.append(new_comb)
                                
                        active_combinations = new_active_combinations
                else:
                    break

     
            switch_index_progress = switch_index
                   
        # Maximum switch progress indicates there were no "breaks"
        if switch_index_progress == len(combination) - 1:
            combination_edits += active_combinations
        
    return combination_edits

   


result = get_item_binary_combinations(ims["item_0"])


print(result)









