from threading import Lock

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0
        self.lock = Lock()  # Create a new lock
               
 # We're creating a new Node and setting its next pointer to the current top of the stack. 
 # If the stack is empty, self.top will be None. Therefore, for an empty stack, the next 
 # pointer of the new node will be set to None, which is correct because there are no other
 # nodes in the stack.
#Then, we're setting self.top to the new node, so the new node becomes the top of the stack. 
    def push(self, value):
        with self.lock:
            node = Node(value)
            node.next = self.top
            self.top = node
            self.size += 1
            # The lock is automatically released when exiting the "with" block
        
    def pop(self):
        with self.lock:
            if self.isEmpty():
                raise Exception("Stack is already empty")
            removedValue = self.top.value
            self.top = self.top.next
            self.size -= 1
            return removedValue
    
    def peek(self):
        with self.lock:
            if self.isEmpty():
                raise Exception("Stack is already empty")
            return self.top.value
        
    def isEmpty(self):
        return self.size == 0


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next
        