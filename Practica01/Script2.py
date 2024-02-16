# Valleys problem solution
def count_valleys(path):
    altitude = 0
    valleys = 0
    for step in path:
        if step == "U":
            altitude += 1
            if altitude == 0:
                valleys += 1
        else:
            altitude -= 1
    return valleys

# Node Class
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Binary Tree Class
class BinarySearchTree:
    def __init__(self):
        self.root = None
    def add(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            current_node = self.root
            while True:
                if value < current_node.value:
                    if current_node.left is None:
                        current_node.left = Node(value)
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.right = Node(value)
                        break
                    else:
                        current_node = current_node.right
    # Preorder Traversal                  
    def preorder_traversal(self):
        return self._preorder_traversal(self.root)

    def _preorder_traversal(self, node):
        if node is None:
            return []
        return [node.value] + self._preorder_traversal(node.left) + self._preorder_traversal(node.right)
    # Inorder Traversal
    def inorder_traversal(self):
        return self._inorder_traversal(self.root)

    def _inorder_traversal(self, node):
        if node is None:
            return []
        return self._inorder_traversal(node.left) + [node.value] + self._inorder_traversal(node.right)
    # Postorder Traversal
    def postorder_traversal(self):
        return self._postorder_traversal(self.root)

    def _postorder_traversal(self, node):
        if node is None:
            return []
        return self._postorder_traversal(node.left) + self._postorder_traversal(node.right) + [node.value]
