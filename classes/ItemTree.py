# -*- coding: utf-8 -*-

GE_METHOD = 'purchased_from_ge'

def get_indent_from_level(level):
    if level == 0:
        return ""
    elif level == 1:
        return "|--"
    else:
        return ((level-1) * "   ") + "|--"

class ItemNode:
        
    # Initializer / Instance Attributes
    def __init__(self, item_id, item_name, quantity, method_members, method=GE_METHOD, method_skills=[]):
        self.item_id = item_id
        self.item_name = item_name
        self.quantity = quantity
        self.method = method
        self.method_members = method_members
        self.method_skills = method_skills
        self.children = []
        
    def __repr__(self):
        return f"<ItemNode:{self.get_id()}>"
        
    def add_child(self, item_node):        
        # Children quantity in method must be equal required parent amount
        new_quantity = self.quantity  * item_node.quantity
        item_node.quantity = new_quantity
        
        self.children.append(item_node)
        
    def is_leaf(self):
        return len(self.children) == 0
       
    def render(self, level=0):        
        indent = get_indent_from_level(level)            
        result = [f"{indent}x{self.quantity} {self.item_name} {self.method}"]
        for child in self.children:
            result.append(child.render(level+1))
        result = '\n'.join(result)
        return result
    
    def render_method(self, level=0):        
        indent = get_indent_from_level(level)            
        result = [f"{indent}{self.method}"]   
        for child in self.children:
            if not child.is_leaf():
                result.append(child.render_method(level+1))
        result = '\n'.join(result)
        return result
        
    def get_friendly_id(self):
        ret = "{}-{}-{}_".format(str(self.quantity), self.item_id, self.method)
        for child in self.children:
            ret += child.get_friendly_id()
        return ret
    
    def get_id(self):
        return str(abs(hash(self.get_friendly_id())))
    
    def clone(self):
        clone = ItemNode(self.item_id, self.item_name, self.quantity, 
                         self.method_members, self.method, self.method_skills)
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
    
    def get_nodes(self):
        nodes = [self]
        for child in self.children:
            nodes += child.get_nodes()
        return nodes
    
    def get_members(self):
        members = False
        nodes = self.get_nodes()        
        for node in nodes:
            members = members or node.method_members
        return members
    
    def get_skill_data(self):
        skill_data = {}
        nodes = self.get_nodes()        
        for node in nodes:
            if node.method != GE_METHOD:
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
    
    def get_required_items(self):
        items = []
        
        # First check if item itself is item we need to purchase
        if self.is_leaf and self.method == GE_METHOD:
            items.append({
                'id': self.item_id,
                'name': self.item_name,
                'quantity': self.quantity
            })            
        
        # Then gather info on children
        leaves = self.get_leaves()
        for leaf in leaves:
            if leaf.method == GE_METHOD:
                items.append({
                    'id': leaf.item_id,
                    'name': leaf.item_name,
                    'quantity': leaf.quantity
                })
        
        return items
    
    def get_required_items_ge_data(self, ge_data):
        items = self.get_required_items()
        for item in items:
            item_id = item['id']
            item['cost'] = ge_data[item_id]['current']
            item['amount_traded_180'] = ge_data[item_id]['amount_traded_180']
            item['daily_price_180'] = ge_data[item_id]['daily_price_180']
        
        return items
    
    
    
class TreeBuilder:
    
    # Initializer / Instance Attributes
    def __init__(self):
        pass

    def create_all(self, all_skill_data, all_item_data):
                
        all_trees = {}
        new_trees = []

        # Create all root trees
        for item_id in all_skill_data:
            item = all_skill_data[item_id]
            
            # Before we go through crafting methods, add the method of obtaining
            # the item from the GE to identify any quick high alch wins.
            item_node = ItemNode(item["id"], item["name"], 1, all_item_data[item_id]['members'], GE_METHOD)
            item_node_id = item_node.get_id()
            all_trees[item_node_id] = item_node
            new_trees.append(item_node_id)
            
            for method in item["methods"]:
                item_node = ItemNode(item["id"], item["name"], 1, method["members"], 
                                     method["name"], method["skills"])
                for material in method["materials"]:
                    material_id = material["id"]
                    material_name = all_item_data[material_id]["name"]
                    material_members = all_item_data[material_id]["members"]
                    child_node = ItemNode(material_id, material_name, material["quantity"], material_members)
                    item_node.add_child(child_node)
                item_node_id = item_node.get_id()
                all_trees[item_node_id] = item_node
                new_trees.append(item_node_id)

        
        
        # Loop through all new trees, finding leafs, growing them.
        while len(new_trees) > 0:
            trees = new_trees
            new_trees = []
            for tree_id in trees:
                tree = all_trees[tree_id]
                leaves = tree.get_leaves()
                for leaf in leaves:
                    leaf_id = leaf.get_id()
                    item_id = leaf.item_id
                           
                    if item_id in all_skill_data:
                                   
                        item = all_skill_data[item_id]
                        
                        for method in item["methods"]:
                            
                            method_name = method['name']
                            method_skills = method['skills']
                        
                            # We create a clone so as to not alter the original tree
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
                                        material_name = all_item_data[material_id]["name"]
                                        material_members = all_item_data[material_id]["members"]
                                        child_node = ItemNode(material_id, material_name, 
                                                              material["quantity"], material_members)
                                        clone_leaf.add_child(child_node)
                                                               
                                    # Save cloned tree to new_trees
                                    clone_tree_id = clone_tree.get_id()
                                    if clone_tree_id not in all_trees:                                                        
                                        all_trees[clone_tree_id] = clone_tree                        
                                        new_trees.append(clone_tree_id)
                                        
        return all_trees

















