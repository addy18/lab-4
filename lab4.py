class BTreeNode:
    def __init__(self, key):
        self.key = key
        self.parent = None


class BTree:
    def __init__(self):
        self.root = None

    def bt_split(self, node):
        if node is not full:
            return None
        node_parent = node.parent
        split_left = BTreeNode(node.a, node.left, node.middle1)
        split_right = BTreeNode(node.c, node.middle2, node.right)
        if node_parent is not None:
            self.insert_key_children(node_parent, node.b, split_left, split_right)
        else:
            node_parent = BTreeNode(node.b, split_left, split_right)
            self.root = node_parent
        return node_parent

    def insert_key_children(self, parent, key, left_child, right_child):
        if key < parent.a:
            parent.c = parent.c
            parent.b = parent.a
            parent.a = key
            parent.right = parent.middle2
            parent.middle2 = parent.middle1
            parent.middle1 = right_child
            parent.left = left_child
        elif parent.b is None or key < parent.b:
            parent.c = parent.b
            parent.b = key
            parent.right = parent.middle2
            parent.middle2 = right_child
            parent.middle1 = left_child
        else:
            parent.c = key
            parent.right = right_child
            parent.middle2 = left_child

    def insert(self, node, key):
        if key in node:
            return None
        if node is full:
            node = self.bt_split(node)
        if node is not leaf:
            if key < node.a:
                return self.insert(node.left, key)
            elif node.a is None or key < node.b:
                return self.insert(node.middle1, key)
            elif node.c is None or key < node.c:
                return self.insert(node.middle1, key)
            else:
                return self.insert(node.right, key)
        else:
            self.insert_into_leaf(node, key)
            return node

    def remove(self, node, key_index):
        if key_index is 0:
            node.a = node.b
            node.b = node.c
            node.c = None
            node.left = node.middle1
            node.middle1 = node.middle2
            node.middle2 = node.right
            node.right = None
        elif key_index is 1:
            node.b = node.c
            node.c = None
            node.middle2 = node.right
            node.right = None
        elif key_index is 2:
            node.c = None
            node.right = None

    def rotate_left(self, node):
        left_s = get_left(node)
        key_left = get_parent_left(node.parent, node)
        self.add_key_and_child(left_s, key_left, node.left)
        self.set_parent_left_key(node.parent, node, node.a)
        self.remove(node, 0)

    #right same as left
    def min_key(self, node):
        curr = node
        while curr.left is not None:
            curr = curr.left
        return curr.a

    def get_child(self, node, child_index):
        if child_index is 0:
            return node.left
        elif child_index is 1:
            return node.middle1
        elif child_index is 2:
            return node.middle2
        elif child_index is 3:
            return node.right
        else:
            return None

    def next_node(self, node, key):
        if key < node.a:
            return node.left
        elif node.b is None or key < node.b:
            return node.middle1
        elif node.c is None or key < node.c:
            return node.middle2
        else:
            return node.right

    def keyswap(self, node, existing, replace):
        if node is None:
            return False
        key_index = self.get_key(node, existing)
        if key_index is -1:
            next = self.next_node(node, existing)
            return self.keyswap(next, existing, replace)
        if key_index is 0:
            node.a = replace
        elif key_index is 1:
            node.b = replace
        else:
            node.c = replace
        return True
