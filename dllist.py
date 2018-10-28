# Doubly-linked list implementation

# 
# Modify this file
#

class NoSuchLink(Exception):
    pass

# A double link has three fields
#  - data <-- The underlying data the link is storing
#  - back <-- A reference to the previous element
#             (possibly None)
#  - next <-- A reference to the next element
#             (possibly None)
class DoubleLink:
    def __init__(self,data,back,nxt):
        self.data    = data
        self.prevLnk = back
        self.nextLnk = nxt

    # Make this object work with "deep" equality. See this
    # StackOverflow post:
    #     https://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes-in-python
    def __eq__(self, other): 
        if (other):
            return self.__dict__ == other.__dict__
        return False

    def hasNext(self):
        return (self.nextLnk != None)
    
    def hasPrev(self):
        return (self.prevLnk != None)

    def getData(self):
        return self.data

    def getNext(self):
        return self.nextLnk

    def getPrev(self):
        return self.prevLnk

    def setNext(self, n):
        self.nextLnk = n

    def setPrev(self, n):
        self.prevLnk = n

# A doubly-linked list
# 15 points
class DLList:
    # Constructor for empty doubly-linked list
    def __init__(self):
        self.first = None

    # Calculate the size of the list
    #  1 points
    def size(self):
        return

    # Check whether this doubly-linked list is equal to another
    # list. Two lists should be equal when they contain exactly the
    # same sequence of elements, where the comparison of each object
    # happens using the == operator.
    # 
    # I.e., two lists (e.g., created using distinct calls to the
    # DoublyLinkedList constructor and subsequent calls to add)
    # containing the sequence of elements: 
    # 
    #   (1,1), (0,1), (1,0)
    # 
    # Should be equal
    #   2 points
    def __eq__(self, other): 
        return

    # Add some data at the head of a doubly-linked list This should
    # take O(1) time
    #   2 points
    def add(self, data):
        return

    # Remove some piece of data from the list. Compare for equality of
    # data using ==
    #   2 points
    def remove(self,data):
        return

    # Check whether the list contains `data`
    #   2 points
    def contains(self, data):
        return

    # Reverse this linked-list in place. After a call to reverse, the
    # last element of the list should become the first, etc...
    #   2 points
    def reverse(self):
        return

    # Convert the elements of this list to an array
    #  2 points
    def toArray(self):
        return

    # Get the `i`th element of the list
    # Precondition: i < self.size()
    # Otherwise, raise NoSuchElementException
    #  2 points
    def getIth(self, i):
        return
