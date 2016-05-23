from tree20jan import *

def toPlain(node):
    return {
        'char': node.char,
        'freq': node.freq,
        'children': [toPlain(child) for child in node.children]
    }

def toNode(dict):
    
    node = Node(dict['char'])
    node.freq = dict['freq']
    for child in dict['children']:
        childNode = toNode(child)
        childNode.parent = node
        node.children.append(childNode)       
    return node

def build(data):
    
    tree = Tree(suffix)
    tree.root = toNode(data)
    return tree
