class Node:
    def __init__(self, value):
        self.value = value
        self.next = None



class LinkedQ:
    def __init__(self):
        self.first = None
        self.last = None

    def isEmpty(self):
        return self.first is None

    def enqueue(self, data):
        new_node = Node(data) # Creates a new nod with Nodes class, the data sets the attr value to data
        if self.isEmpty():  # If the queue is empty set both attr to new_node
            self.first = new_node
            self.last = new_node
        else:  # if there is already nodes inside
            self.last.next = new_node  # link new node to the last one
            self.last = new_node  # Update so that the new node is the last node

    def dequeue(self):
        if self.isEmpty():
            print("The list is empty")
            return
        else:
            node_remove = self.first
            self.first = self.first.next
            return node_remove.value # We need to access the value so that it is not a Node object
    
    def peek(self):
        if not self.isEmpty():
            return self.first.value
    