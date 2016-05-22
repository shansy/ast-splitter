# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from math import sqrt


def suffix(s):
    return [s[i:] for i in range(len(s))]

def radix(s):
    return [s]

def search(s, root, path, lvl = 0):
    for n in root.children:
        if n.char == s[lvl]:
            path.append(n)
            search(s, n, path, lvl + 1)

def collect_leaf_nodes(node, leafs):
    if len(node.children) == 0:
            leafs.append(node)
    for n in node.children:
        collect_leaf_nodes(n, leafs)


def print_tree(root, lvl=0):
        print u' '*lvl + root.char + u' ' + str(root.freq) 
        for i in root.children:
            print_tree(i, lvl+1)

class Node():
    def __init__(self, char):
        self.char = char
        self.freq = .0
        self.parent = None
        self.children = []
        self.isLeaf = False
        self.max_freq = .0
        self.min_freq = .0


class Tree():
    def __init__(self, repr):
        self.root = Node(u'root')
        self.repr = repr
        self.scoring = .0
        self.scores = []
        self.leaves = []
        self.chains = []
    def search(self, s):
        path = []
        search(s, self.root, path)
        return path
    def add(self, s, freq = 1.0):
        subs = self.repr(s+u'$')
        for sub in subs:
            path = self.search(sub)
            if len(path) == 0:
                cN = self.root
                self.root.freq += freq
                pos = 0
            else:
                self.root.freq += freq
                for n in path: n.freq += freq
                cN = path[-1]
                pos = len(path)
            for c in sub[pos:]:
                nN = Node(c)
                nN.freq += freq
                nN.parent = cN
                cN.children.append(nN)
                cN = nN


    def myprint(self):
        print_tree(self.root)

def find_paths2(leaf,  path, paths, thrsh1 = 10, thrsh2 = 15000, len_thrsh = 4):
    if leaf.freq > thrsh1:
        if not leaf.char == u'$':
            path += leaf.char
        if not leaf.parent.in_path and leaf.parent.freq < thrsh2:
            print  path
            find_paths2(leaf.parent, path, paths)
        else:
            if not path[::-1] in paths and len(path) >= len_thrsh:
                paths.append(path[::-1])
    else:
        find_paths2(leaf.parent, path, paths)




def subtree(t1, t2, new_tree, node1, node2, cN):
    '''
    t3 is the  result
    '''
    for ch1 in node1.children:
        for ch2 in node2.children:
            if ch1.char == ch2.char:
                if ch1.parent == t1.root:
                    cN = new_tree.root
                    new_tree.root.max_freq = max(t1.root.freq, t2.root.freq)
                    new_tree.root.min_freq = min(t1.root.freq, t2.root.freq)
                nN = Node(ch1.char)
                nN.max_freq = max(ch1.freq, ch2.freq)
                nN.min_freq = min(ch1.freq, ch2.freq)
                nN.parent = cN
                cN.children.append(nN)
                if cN in new_tree.leaves:
                    new_tree.leaves.remove(cN)
                new_tree.leaves.append(nN)
                cN = nN
                subtree(t1, t2, new_tree, ch1, ch2, cN)
