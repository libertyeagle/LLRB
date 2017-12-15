class Node():
    def __init__(self, key, val, N, color):
        self.__key = key
        self.__val = val
        self.__N = N
        self.__left = None
        self.__right = None
        self.__color = True # True means RED, False means BLACK
    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, parameter):
        self.__key = parameter

    @property
    def val(self):
        return self.__val

    @val.setter
    def val(self, parameter):
        self.__val = parameter

    @property
    def N(self):
        return self.__N

    @N.setter
    def N(self, parameter):
        self.__N = parameter

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, parameter):
        self.__left = parameter

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, parameter):
        self.__right = parameter

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, parameter):
        self.__color = parameter

class RedBlackBST():
    def __init__(self):
        self.root=None

    def __realsize(self,x):
        if x is None:
            return 0
        else:
            return x.N

    def size(self):
        return self.__realsize(self.root)

    def __isRed(self,x):
        if x is None:
            return False
        else:
            return x.color

    def __rotateLeft(self, x):
        h=x.right
        x.right=h.left
        h.left=x
        h.color=x.color
        x.color=True
        h.N=x.N
        x.N=self.__realsize(x.left)+self.__realsize(x.right)+1
        return h

    def __rotateRight(self, x):
        h = x.left
        x.left = h.right
        h.right = x
        h.color=x.color
        x.color=True
        h.N = x.N
        x.N = self.__realsize(x.left) + self.__realsize(x.right) + 1
        return h

    def __flipColors(self,x):
        x.color=not x.color
        x.left.color=not x.left.color
        x.right.color=not x.right.color

    def isEmpty(self):
        return self.root is None

    def get(self,key):
        x=self.root
        while not (x is None):
            if key<x.key:
                x=x.left
            elif key>x.key:
                x=x.right
            else:
                return x.val
        return None

    def __rput(self, x, key, value):
        if x is None:
            return Node(key,value,1,True)
        if key<x.key:
            x.left=self.__rput(x.left,key,value)
        elif key>x.key:
            x.right=self.__rput(x.right,key,value)
        else:
            x.val=value
        # There are three cases we need to consider to maintain the property of Red-Black BST
        if (self.__isRed(x.right)) and (not self.__isRed(x.left)):
            x=self.__rotateLeft(x)
        if (self.__isRed(x.left)) and (self.__isRed(x.left.left)):
            x=self.__rotateRight(x)
        if (self.__isRed(x.left)) and (self.__isRed(x.right)):
            self.__flipColors(x)
        x.N = self.__realsize(x.left) + self.__realsize(x.right) + 1
        return x

    def put(self,key,value):
        self.root=self.__rput(self.root,key,value)
        self.root.color=False # We need to keep the root BLACK

    # moveRedLeft make h.left or h.left.left RED, depending on whether h.right.left is RED
    # Nodes below h (or say h's children) satisfy all properties of a RBTree, there's no chance that h.left.right is RED
    def __moveRedLeft(self,x):
        self.__flipColors(x)
        if self.__isRed(x.right.left):
            x.right=self.__rotateRight(x.right)
            x=self.__rotateLeft(x)
            self.__flipColors(x)
        return x

    # moveRedRight make h.right or h.right.right RED, depending on whether h.left.left is RED
    def __moveRedRight(self,x):
        self.__flipColors(x)
        if self.__isRed(x.left.left):
            x=self.__rotateRight(x)
            self.__flipColors(x)
        return x

    # This function is used to maintain properties of RBTree, cleaning up all remaining 4-nodes when we go up
    def __balance(self,x):
        # We check the same things as in the function put()
        if self.__isRed(x.right):   # This is equivalent to 'if (self.__isRed(x.right)) and (not self.__isRed(x.left)):'
            x=self.__rotateLeft(x)
        if (self.__isRed(x.left)) and (self.__isRed(x.left.left)):
            x=self.__rotateRight(x)
        if (self.__isRed(x.left)) and (self.__isRed(x.right)):
            self.__flipColors(x)
        x.N = self.__realsize(x.left) + self.__realsize(x.right) + 1
        return x

    def __deleteMin(self, x):
        if x.left is None:
            return None
        # If both x.left and x.left.left is BLACK, we need to make one of them RED, so that we can pass on
        if (not self.__isRed(x.left)) and (not self.__isRed(x.left.left)):
            x=self.__moveRedLeft(x)
        x.left=self.__deleteMin(x.left)
        return self.__balance(x)

    def __deleteMax(self, x):
        if self.__isRed(x.left):
            x=self.__rotateRight(x)
        if x.right is None:
            return None
        # Notice that it is x.right.left, not x.right.right, because it's a left-lean RBTree
        if (not self.__isRed(x.right)) and (not self.__isRed(x.right.left)):
            x=self.__moveRedRight(x)
        x.right=self.__deleteMax(x.right)
        return self.__balance(x)

    def deleteMin(self):
        # We can notice that root.left and root.right cannot all be RED at the same time
        # So following statement is equivalent to 'if not self.__isRed(self.root.left):'
        if (not self.__isRed(self.root.left)) and (not self.__isRed(self.root.right)):
            self.root.color=True
        self.root=self.__deleteMin(self.root)
        if not self.isEmpty():
            self.root.color=False

    def deleteMax(self):
        if (not self.__isRed(self.root.left)) and (not self.__isRed(self.root.right)):
            self.root.color=True
        self.root=self.__deleteMax(self.root)
        if not self.isEmpty():
            self.root.color=False

    def __realmin(self,x):
        if x.left is None:
            return x
        else:
            return self.__realmin(x.left)

    def min(self):
        return self.__realmin(self.root).key

    def __realmax(self, x):
        if x.right is None:
            return x
        else:
            return self.__realmax(x.right)

    def max(self):
        return self.__realmax(self.root).key

    def __rfloor(self,x,key):
        if x is None:
            return None
        if key<x.key:
            return self.__rfloor(x.left,key)
        elif key>x.key:  # x.key may not be the largest key smaller than key, so we continue to search in right subtree
            t=self.__rfloor(x.right,key)
            if not (t is None):
                return t
            else:
                return x
        else:
            return x

    def floor(self,key):
        x=self.__rfloor(self.root,key)
        if x is None:
            return None
        else:
            return x.key

    def __rceiling(self, x, key):
        if x is None:
            return None
        if key > x.key:
            return self.__rceiling(x.right,key)
        elif key < x.key:
            t = self.__rceiling(x.left,key)
            if not (t is None):
                return t
            else:
                return x
        else:
            return x

    def ceiling(self, key):
        x = self.__rceiling(self.root,key)
        if x is None:
            return None
        else:
            return x.key

    def __rselect(self,x,k):
        if x is None:
            return None
        t=self.__realsize(x.left)
        if t<k:
            return self.__rselect(x.right,k-t-1)   # Search in right subtree
        elif t>k:
            return self.__rselect(x.left,k)    # Search in left subtree
        else:
            return x

    def select(self,k):
        x=self.__rselect(self.root,k)
        if not (x is None):
            return x.key
        else:
            return None

    def __rrank(self,x,key):
        if x is None:
            return 0
        if key<x.key:
            return self.__rrank(x.left,key)
        elif key>x.key:
            return self.__rrank(x.right,key)+self.__realsize(x.left)+1
        else:
            return self.__realsize(x.left)

    def __delete(self,x,key):
        if key<x.key:
            if (not self.__isRed(x.left)) and (not self.__isRed(x.left.left)):
                x=self.__moveRedLeft(x)
            x.left=self.__delete(x.left,key)
        else:
            if self.__isRed(x.left):
                x=self.__rotateRight(x)
            if x.key==key and x.right is None:  # x.right is None, we can simply delete the node
                return None
            if (not self.__isRed(x.right)) and (not self.__isRed(x.right.left)):
                x=self.__moveRedRight(x)
            if key==x.key:  # Exchange x with x's successor
                h=self.__realmin(x.right)
                x.key=h.key
                x.val=h.val
                x.right=self.__deleteMin(x.right)
            else:
                x.right=self.__delete(x.right,key)
        return self.__balance(x)

    def delete(self,key):
        if (not self.__isRed(self.root.left)) and (not self.__isRed(self.root.right)):
            self.root.color=True
        self.root=self.__delete(self.root,key)
        if not self.isEmpty():
            self.root.color=False

    def rank(self,key):
        return self.__rrank(self.root,key)

    def __llrbprint(self,x):
        if x is None:
            return
        self.__llrbprint(x.left)
        color={True:"RED",False:"BLACK"}
        print('Key:',x.key,'Value:',x.val,'Color:',color[x.color])
        self.__llrbprint(x.right)

    def llrbprint(self):
        self.__llrbprint(self.root)