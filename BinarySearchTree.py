from Node import Node
import threading


def find_replacement(node):
    # finds right most node of left subtree
    curr = node.left
    pred = node
    while True:
        if curr.right is not None:
            pred = curr
            curr = curr.right
        else:
            break
    return pred, curr


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.tree_lock = threading.Lock()

    def add(self, elem):
        if self.root is None:
            # Empty tree
            self.root = Node(elem)
            self.size += 1
            return True

        curr = self.root

        while True:
            if elem < curr.elem:
                if curr.left is None:
                    # We found the place to append
                    curr.left = Node(elem)
                    self.size += 1
                    return True
                else:
                    curr = curr.left
            elif elem > curr.elem:
                if curr.right is None:
                    # We found the place to append
                    curr.right = Node(elem)
                    self.size += 1
                    return True
                else:
                    curr = curr.right
            else:
                # a duplicate element is found, we abort
                return False

    def remove(self, elem):
        if self.root is None:
            # Empty tree
            return False

        curr = self.root
        pred = None

        while curr is not None:
            if elem > curr.elem:
                pred = curr
                curr = curr.right
            elif elem < curr.elem:
                pred = curr
                curr = curr.left
            else:
                if curr.left is not None and curr.right is not None:
                    parent, replacement = find_replacement(curr)
                    replacement.right = curr.right
                    if curr == pred.left:
                        pred.left = replacement
                    else:
                        pred.right = replacement
                elif curr.left is None and curr.right is not None:
                    if curr == self.root:
                        self.root = curr.right
                    else:
                        if curr == pred.left:
                            pred.left = curr.right
                        else:
                            pred.right = curr.right
                elif curr.left is not None and curr.right is None:
                    if curr == self.root:
                        self.root = curr.left
                    else:
                        # pred is not None
                        assert pred is not None
                        if curr == pred.left:
                            pred.left = curr.left
                        else:
                            pred.right = curr.left
                else:
                    if curr == self.root:
                        self.root = None
                    else:
                        if curr == pred.left:
                            pred.left = None
                        else:
                            pred.right = None
                self.size -= 1
                return True
        return False
