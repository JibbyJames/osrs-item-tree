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

skill_items = {}

skill_items["Bow"] = {
  "id": "Bow",
  "methods": [{
    "name": "Fletching_assembly",
    "skills": [{
        "name": "fletching",
        "lvl": 40,
        "xp": 50
    }],
    "materials": [{
      "id": "Fletched_Bow_Handle",
      "quantity": 1
    },{
      "id": "Bow_string",
      "quantity": 1
    }]
  }]
}
    
skill_items["Fletched_Bow_Handle"] = {
  "id": "Fletched_Bow_Handle",
  "methods": [{
    "name": "Fletching_carving",
    "skills": [{
        "name": "fletching",
        "lvl": 40,
        "xp": 50
    }],
    "materials": [{
      "id": "Yew_log",
      "quantity": 5
    }]
  }]
}
    
skill_items["Yew_log"] = {
  "id": "Yew_log",
  "methods": [{
    "name": "Woodcutting",
    "skills": [{
        "name": "woodcutting",
        "lvl": 60,
        "xp": 50
    }],
    "materials": []
  }]
}
  
skill_items["Bow_string"] = {
  "id": "Bow_string",
  "methods": [{
    "name": "Spinning",
    "skills": [{
        "name": "crafting",
        "lvl": 10,
        "xp": 15
    }],
    "materials": [{
      "id": "Flax",
      "quantity": 1
    }]
  }]
}
    
skill_items["Flax"] = {
  "id": "Flax",
  "methods": [{
    "name": "flax-picking",
    "skills": [],
    "materials": []
  }]
}
    


class ItemNode:
        
    # Initializer / Instance Attributes
    def __init__(self, name, method, quantity, method_skills=[]):
        self.name = name
        self.quantity = quantity
        self.method = method
        self.method_skills = method_skills
        self.children = []
        
    def __repr__(self):
        return f"<ItemNode:{self.get_id()}>"
        
    def add_child(self, item_node):        
        # Children quantity in method must be equal required parent amount
        new_quantity = int(self.quantity) * int(item_node.quantity)
        item_node.quantity = new_quantity
        
        self.children.append(item_node)
        
    def is_leaf(self):
        return len(self.children) == 0
       
    def render(self, level=0):        
        if level == 0:
            indent = ""
        elif level == 1:
            indent = "|--"
        else:
            indent = ((level-1) * "   ") + "|--"
            
        ret = [f"{indent}x{self.quantity} {self.name} {self.method}"]   
        for child in self.children:
            ret.append( child.render(level+1))
        return '\n'.join(ret)
        
    def get_friendly_id(self):
        ret = "{}-{}-{}_".format(str(self.quantity), self.name, self.method)
        for child in self.children:
            ret += child.get_friendly_id()
        return ret
    
    def get_skill_data(self):
        skill_data = {}
        nodes = self.get_all_nodes()        
        for node in nodes:
            if node.method != "purchased_from_ge":
                node_quantity = node.quantity
                node_skills = node.method_skills
                for skills in node_skills:
                    skill_name = skills["name"]
                    skill_lvl = skills["lvl"]
                    skill_xp = skills["xp"]
                    
                    if skill_name in skill_data:
                        skill_data[skill_name] = {
                            'lvl': max(skill_data[skill_name]["lvl"], skill_lvl),
                            'xp': skill_data[skill_name]["xp"] + (skill_xp * node_quantity)
                        }
                    else:
                        skill_data[skill_name] = {
                            'lvl': skill_lvl,
                            'xp': skill_xp * node_quantity
                        }
        return skill_data
    
    def get_id(self):
        return str(abs(hash(self.get_friendly_id())))
    
    def clone(self):
        clone = ItemNode(self.name, self.method, self.quantity, self.method_skills)
        for child in self.children:
            clone.children.append(child.clone())
        return clone
    
    def get_leaves(self):
        leaves = []
        for child in self.children:
            if child.is_leaf():
                leaves.append(child)
            else:
                leaves += child.get_leaves()
        return leaves
    
    def get_all_nodes(self):
        nodes = [self]
        for child in self.children:
            nodes += child.get_all_nodes()
        return nodes
            

all_trees = {}
new_trees = []

# Create all root trees
for item_id in skill_items:
    item = skill_items[item_id]    
    for method in item["methods"]:
        method_name = method["name"]
        item_node = ItemNode(item["id"], method_name, 1, method["skills"])
        for material in method["materials"]:
            material_id = material["id"]
            material_quantity = material["quantity"]
            material_method = "purchased_from_ge"
            child_node = ItemNode(material_id, material_method, material_quantity)
            item_node.add_child(child_node)
        item_node_id = item_node.get_id()
        all_trees[item_node_id] = item_node
        new_trees.append(item_node_id)

# Loop through all new trees, finding leafs, growing them.
while len(new_trees) > 0:
    
    print('---- New trees ----')
    for tree_id in new_trees:
        print(f'Tree Id: {tree_id}')
        print(all_trees[tree_id].render()) 
        leaves = all_trees[tree_id].get_leaves()
    
        for leaf in leaves:
            print(f'Leaf: {leaf.name}')
                       
        print('\n')   

    trees = new_trees
    new_trees = []
    for tree_id in trees:
        tree = all_trees[tree_id]
        leaves = tree.get_leaves()
        for leaf in leaves:
            leaf_id = leaf.get_id()
            item_id = leaf.name
                   
            if item_id in skill_items:
                           
                item = skill_items[item_id]
                
                for method in item["methods"]:
                    
                    method_name = method['name']
                    method_skills = method['skills']
                
                    # We create a clone so as to not "grow" the original tree
                    clone_tree = tree.clone()
                                    
                    # This does require looping the leaves again
                    clone_leaves = clone_tree.get_leaves()
                    for clone_leaf in clone_leaves:
                        clone_leaf_id = clone_leaf.get_id()
                        
                        if leaf_id == clone_leaf_id:
                            
                            clone_leaf.method = method_name
                            clone_leaf.method_skills = method_skills
                            
                            # Grow leaf
                            for material in method["materials"]:
                                material_id = material["id"]
                                material_quantity = material["quantity"]
                                material_method = "purchased_from_ge"
                                child_node = ItemNode(material_id, material_method, material_quantity)
                                clone_leaf.add_child(child_node)
                                                       
                            # Save cloned tree to new_trees
                            clone_tree_id = clone_tree.get_id()
                            if clone_tree_id not in all_trees:                                                        
                                all_trees[clone_tree_id] = clone_tree                        
                                new_trees.append(clone_tree_id)


print('---- Final trees ----')
for tree_id in all_trees:
    print(f'Tree Id: {tree_id} -------')
    print(all_trees[tree_id].render())
    print(f'Skills: {all_trees[tree_id].get_all_skill_data()}')




















































