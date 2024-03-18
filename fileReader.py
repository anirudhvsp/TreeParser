import tkinter as tk
from tkinter import ttk

def populate_tree(tree, node, parent=''):
    item = tree.insert(parent, 'end', text=node.method_name)
    for child in node.children:
        populate_tree(tree, child, item)

def toggle_children(tree, item):
    children = tree.get_children(item)
    if children:
        for child in children:
            toggle_children(tree, child)
        tree.item(item, open=not tree.item(item, 'open'))


class TreeNode:
    def __init__(self, method_name):
        self.method_name = method_name
        self.children = []

    def print_tree(self, level=0):
        print('  ' * level + self.method_name)
        for child in self.children:
            child.print_tree(level + 1)

def build_tree(data, root_node):
    min_level = min(item['level'] for item in data)
    min_indices = [index for index, item in enumerate(data) if item['level'] == min_level]
    min_elements = [item for index, item in enumerate(data) if item['level'] == min_level]
    separate_lists = []
    
    start_index = 0
    for min_index in min_indices:
        tempList = data[start_index:min_index + 1]
        filtered_data = [x for x in tempList if x not in min_elements]
        separate_lists.append(filtered_data)
        start_index = min_index + 1

    if start_index < len(data):
        tempList = data[start_index:]
        filtered_data = [x for x in tempList if x not in min_elements]
        separate_lists.append(filtered_data)
    

    for i in range(len(min_elements)):
        currentNode = TreeNode(min_elements[i]['methodName'])
        root_node.children.append(currentNode)
        if(len(separate_lists[i])==1):
            currentNode.children.append(TreeNode(separate_lists[i][0]['methodName']))
            return
        else:
            if(len(separate_lists[i])!= 0):
                build_tree(separate_lists[i], currentNode)        



def readFromFile(filename):
    lst = []
    with open(filename, 'r') as file:
        for line in file:
            level, methodName = count_and_strip_spaces(line.split('21')[1])
            lst.append({'level': level,'methodName': methodName})
    return lst

def count_and_strip_spaces(input_string):
    num_spaces = 0
    for char in input_string:
        if char == ' ':
            num_spaces += 1
        else:
            break
    return num_spaces, input_string.strip().split('|')[0]

data = readFromFile('temp2.txt')
rootNode = TreeNode("Root")
build_tree(data, rootNode)
root = tk.Tk()
root.title("Tree Display")
tree = ttk.Treeview(root)
tree.pack(expand=True, fill=tk.BOTH)
populate_tree(tree, rootNode)

root.mainloop()