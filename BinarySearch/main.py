class binarySearchTree:

    def __init__(self, val = None):

        self.val = val
        self.left = None
        self.right = None

    def insert(self, val) -> None: # key - self.val
        # Перевірка на рут
        if (self.val == None):
            self.val = val
        # Перевірка позиції на вставку елемента
        else:
            # Перевірка на дублікати
            if val == self.val: 
                return 'Знайдені дублікати!'
            # Перевырка чи значення яке ми вставляэмо менше за поточне значення вузла
            if (val < self.val):
                # перевіка чи є лівий вузол для поточного значення
                if(self.left):
                    self.left.insert(val)
                # вставити ліворуч від поточного вузла, коли currentNode.left=None
                else: 
                    self.left = binarySearchTree(val)

            # ті самі дії що й вище, тут умова, яку ми перевіряємо: якщо значенням inserted > currentNode's value
            else:
                if(self.right):
                    self.right.insert(val)
                else: 
                    self.right = binarySearchTree(val)

    def find(self, val, parent=None):
        # повертаючи вузол і його батьківський вузол
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

    def remove(self, val):

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

    def find_conprasion(self):
        currentNode = self
        bfs_list = []
        queue = []
        queue.insert(0,currentNode)
        while(len(queue) > 0):
            currentNode = queue.pop()
            bfs_list.append(currentNode.val)
            if(currentNode.left):
                queue.insert(0,currentNode.left)
            if(currentNode.right):
                queue.insert(0,currentNode.right)

        return bfs_list

    def inorder(self):
        return self.traverseInOrder([])

    def preorder(self):
        return self.traversePreOrder([])

    def postorder(self):
        return self.traversePostOrder([])

    def return_min_key(self):
        current = self
        while current.left is not None:
            current = current.left
        return current.val

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


bst = binarySearchTree()
bst.insert(7)
bst.insert(4)
bst.insert(9)
bst.insert(0)
bst.insert(5)
bst.insert(8)
bst.insert(13)

#         7
#       /   \
#      /     \
#     4       9
#    / \    /  \
#   0   5  8    13


print('IN order: ', bst.inorder())
print('PRE order:', bst.preorder())
print('POST order:', bst.postorder())
print(bst.remove(5))
print(bst.remove(9))
print(bst.remove(7))

# after deleting
print('IN order: ',bst.inorder())