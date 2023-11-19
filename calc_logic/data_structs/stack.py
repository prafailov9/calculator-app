from threading import Lock

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0
        self.lock = Lock()
               
 
    def push(self, value):
        with self.lock:
            node = Node(value)
            node.next = self.top
            self.top = node
            self.size += 1
        
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
        