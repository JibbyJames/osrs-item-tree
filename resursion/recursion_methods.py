skill_items = {}

skill_items["0"] = {
  "id": "0",
  "methods": [{
    "name": "zero",
    "materials": [{
      "id": "1",
      "quantity": 1
    }]
  }]
}
    
skill_items["1"] = {
  "id": "1",
  "methods": [{
    "name": "one",
    "materials": [{
      "id": "2",
      "quantity": 1
    }]
  }]
}
    
skill_items["2"] = {
  "id": "2",
  "methods": [{
    "name": "two",
    "materials": [{
      "id": "3",
      "quantity": 1
    }]
  }]
}
    
skill_items["3"] = {
  "id": "3",
  "methods": [{
    "name": "three",
    "materials": [{
      "id": "4",
      "quantity": 1
    }]
  }]
}
    
all_items = {}

all_items["0"] = {"id": "item_0"}
all_items["1"] = {"id": "item_1"}
all_items["2"] = {"id": "item_2"}
all_items["3"] = {"id": "item_3"}
all_items["4"] = {"id": "item_4"}

    
def get_binary_combinations(num_of_digits):
    
    binary_combinations = []
    
    if num_of_digits == 0:
        return binary_combinations
    
    # Get largest possible binary number of X digits
    max_num_binary = num_of_digits * "1"
    max_num = int(max_num_binary, 2)
            
    # Pattern adds leading zeros to keep digit count consistent
    pattern = '0{}b'.format(num_of_digits)
    
    # Count from 0 to max_num, representing all combinations.
    for i in range(0, max_num + 1):
        binary_combinations.append(format(i, pattern))
    
    return binary_combinations


def get_child_combinations(method_id):
    method = all_method_tree[method_id]    
    count_of_children = len(method["children"])    
    return get_binary_combinations(count_of_children)

def has_children(method):
    return("children" in method) and (len(method["children"]) > 0)

# Create flat dict of all methods. Key = item_method
all_methods = {}
for item_id in skill_items:
    item = skill_items[item_id]
    for method in item["methods"]:
        method_name = method["name"]
        new_method_name = "{}_{}".format(item_id, method_name)
        all_methods[new_method_name] = method

all_method_tree = {}
for method_id in all_methods:
    all_method_tree[method_id] = {"id": method_id, "children": []}
    method = all_methods[method_id]
    for material in method["materials"]:
        material_id = material["id"]
        if material_id in skill_items:

            for material_method in skill_items[material_id]["methods"]:
                material_method_name = material_method["name"]
                main_method_name = "{}_{}".format(material_id, material_method_name)
                
                if main_method_name in all_methods:
                    all_method_tree[method_id]["children"].append(main_method_name)
                    
        else:
            all_method_tree[method_id]["children"].append(material_id)




