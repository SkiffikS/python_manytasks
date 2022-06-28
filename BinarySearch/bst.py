from typing import Any, Generator, Tuple
from main import binarySearchTree

from tree_node import TreeNode


class BinarySearchTree:
    """Binary-Search-Tree implemented for didactic reasons."""
    def __init__(self, root: TreeNode = None):
        #Initialize BinarySearchTree.

        self.val = TreeNode
        self.left = None
        self.right = None
        self._root = root
        self._size = 0 if root is None else 1

    def insert(self, key: int, value: Any) -> None:
        """Insert a new node into BST."""
        if (self.val == None):
            self.val = value
        # Перевірка позиції на вставку елемента
        else:
            # Перевірка на дублікати
            if value == self.val:
                return 'Знайдені дублікати!'
            # Перевырка чи значення яке ми вставляэмо менше за поточне значення вузла
            if (value < self.val):
                # перевіка чи є лівий вузол для поточного значення
                if(self.left):
                    self.left.insert(value)
                # вставити ліворуч від поточного вузла, коли currentNode.left=None
                else:
                    self.left = binarySearchTree(value)

            # ті самі дії що й вище, тут умова, яку ми перевіряємо: якщо значенням inserted > currentNode's value
            else:
                if(self.right):
                    self.right.insert(value)
                else:
                    self.right = binarySearchTree(value)

    def find(self, key: int, val, parent=None) -> TreeNode:
        """Return node with given key."""

        if val == self.val:
            return self, parent
        if (val < self.val):
            if (self.left):
                return self.left.find(val, self)
            else:
                return "Вузол не знайдено"
        else:
            if (self.right):
                return self.right.find(val, self)
            else:
                return "Вузол не знайдено"

    @property
    def size(self) -> int:
        """Return number of nodes contained in the tree."""
        pass
        # TODO

    # If users instead call `len(tree)`, this makes it return the same as `tree.size`
    __len__ = size 

    # This is what gets called when you call e.g. `tree[5]`
    def __getitem__(self, key: int) -> Any:
        """Return value of node with given key.

        Args:
            key (int): Key to look for.

        Raises:
            ValueError: If key is not an integer.
            KeyError: If key is not present in the tree.

        Returns:
            Any: [description]
        """
        return self.find(key).value

    def remove(self, key: int, val) -> None:
        """Remove node with given key, maintaining BST-properties."""
        if(self.find(val) == "Вузол не знайдено"):
            return "Вузол не в дереві"

        deleteing_node, parent_node = self.find(val)

        nodes_effected = deleteing_node.traversePreOrder([])

        if (len(nodes_effected) == 1):
            if (parent_node.left.val == deleteing_node.val):
                parent_node.left = None
            else:
                parent_node.right = None
            return "Успішно видалено"

        else:

            if (parent_node == None):
                nodes_effected.remove(deleteing_node.val)

                self.left = None
                self.right = None
                self.val = None

                for node in nodes_effected:
                    self.insert(node)
                return "Успішно видалено"

            nodes_effected = parent_node.traversePreOrder([])

            if (parent_node.left == deleteing_node):
                parent_node.left = None
            else:
                parent_node.right = None

            nodes_effected.remove(deleteing_node.val)
            nodes_effected.remove(parent_node.val)
            for node in nodes_effected:
                self.insert(node)

        return "Успішно видалено"
       
    # Hint: The following 3 methods can be implemented recursively, and 
    # the keyword `yield from` might be extremely useful here:
    # http://simeonvisser.com/posts/python-3-using-yield-from-in-generators-part-1.html

    # Also, we use a small syntactic sugar here: 
    # https://www.pythoninformer.com/python-language/intermediate-python/short-circuit-evaluation/

    def inorder(self, node: TreeNode = None) -> Generator[TreeNode, None, None]:
        """Yield nodes in inorder."""
        node = node or self._root
        # This is needed in the case that there are no nodes.
        if not node:
            return iter(())
        pass
        # TODO

    def preorder(self, node: TreeNode = None) -> Generator[TreeNode, None, None]:
        """Yield nodes in preorder."""
        node = node or self._root
        if not node:
            return iter(())
        pass
        # TODO

    def postorder(self, node: TreeNode = None) -> Generator[TreeNode, None, None]:
        """Yield nodes in postorder."""
        node = node or self._root
        if not node:
            return iter(())
        pass
        # TODO

    # this allows for e.g. `for node in tree`, or `list(tree)`.
    def __iter__(self) -> Generator[TreeNode, None, None]: 
        yield from self._preorder(self._root)

    @property
    def is_valid(self) -> bool:
        """Return if the tree fulfills BST-criteria."""
        pass
        # TODO

    def return_min_key(self) -> TreeNode:
        """Return the node with the smallest key (None if tree is empty)."""
        pass
        # TODO
           
    def find_comparison(self, key: int) -> Tuple[int, int]:
        """Create an inbuilt python list of BST values in preorder and compute the number of comparisons needed for
           finding the key both in the list and in the BST.
           Return the numbers of comparisons for both, the list and the BST
        """
        currentNode = self
        bfs_list = []
        queue = []
        queue.insert(0, currentNode)
        while(len(queue) > 0):
            currentNode = queue.pop()
            bfs_list.append(currentNode.val)
            if(currentNode.left):
                queue.insert(0, currentNode.left)
            if(currentNode.right):
                queue.insert(0, currentNode.right)

    def __repr__(self) -> str:
        return f"BinarySearchTree({list(self._inorder(self._root))})"

    ####################################################
    # Helper Functions
    ####################################################

    def get_root(self):
        return self._root

    def _inorder(self, current_node):
        return self.traverseInOrder([])

    def _preorder(self, current_node):
        return self.traversePreOrder([])

    def _postorder(self, current_node):
        return self.traversePostOrder([])
        # TODO

    def traverseInOrder(self, lst):
        if (self.left):
            self.left.traverseInOrder(lst)
        lst.append(self.val)
        if (self.right):
            self.right.traverseInOrder(lst)
        return lst

    def traversePreOrder(self, lst):
        lst.append(self.val)
        if (self.left):
            self.left.traversePreOrder(lst)
        if (self.right):
            self.right.traversePreOrder(lst)
        return lst

    def traversePostOrder(self, lst):
        if (self.left):
            self.left.traversePostOrder(lst)
        if (self.right):
            self.right.traversePostOrder(lst)
        lst.append(self.val)
        return lst
    # You can of course add your own methods and/or functions!
    # (A method is within a class, a function outside of it.)
