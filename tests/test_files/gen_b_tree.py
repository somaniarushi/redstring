def split_inner_node(self):
    mid = len(self.keys) // 2
    splitKey = self.keys[mid]
    newInnerNode = InnerNode(self.keys[mid+1:], self.children[mid+1:])
    self.keys = self.keys[:mid]
    self.children = self.children[:mid+1]
    return splitKey, newInnerNode

def split_leaf_node(self):
    mid = len(self.keys) // 2
    splitKey = self.keys[mid]
    newLeafNode = LeafNode(self.keys[mid+1:], self.children[mid+1:])
    self.keys = self.keys[:mid]
    self.children = self.children[:mid+1]
    return splitKey, newLeafNode


class BTree:
    def __init__(self, root):
        self.root = root

    def put(self, key):
        ret = self.root.put(key)
        if ret is not None:
            splitKey = ret[0]
            child = ret[1]
            keys = [splitKey]
            children = [self.root, child]
            new_root = InnerNode(keys, children)
            self.update_root(new_root)

    def update_root(self, new_root):
        self.root = new_root

class InnerNode:
    MAX = 4

    def __init__(self, keys, children):
        self.keys = keys
        self.children = children

    def put(self, key):
        self.keys.append(key)
        if len(self.keys) > self.MAX:
            splitKey, newInnerNode = split_inner_node(self, self.keys, self.children)
        return splitKey, newInnerNode

class LeafNode:
    MAX = 4

    def __init__(self, keys, rids):
        self.keys = keys
        self.rids = rids

    def put(self, key):
        self.keys.append(key)
        if len(self.keys) > self.MAX:
            splitKey, newLeafNode = split_leaf_node(self, self.keys, self.children)
        return splitKey, newLeafNode
