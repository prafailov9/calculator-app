from data_structs.stack import Stack

class ExpressionNode :
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class ExpressionTree:
    def __init__(self, postfix_expr):
        self.root = self.build_tree(postfix_expr)

    @staticmethod
    def build_tree(postfix_expr):
        tree_node_stack = Stack()

        for current in postfix_expr.split():
            if current in ('+', '-', '*', '/', '^'):
                # Create a new node for the operator
                node = ExpressionNode(current)

                # Pop two nodes and make them children of the new node
                node.right = tree_node_stack.pop() if not tree_node_stack.isEmpty() else None
                node.left = tree_node_stack.pop() if not tree_node_stack.isEmpty() else None
                
                # if the stack was empty and node.left or node.right is None, then raise an error
                if node.left is None or node.right is None:
                    raise ValueError("The expression is not well formed. Not enough operands for the operators.")
            else:
                # Create a new node for the number and push it to the stack
                node = ExpressionNode(int(current))

            tree_node_stack.push(node)

        # The remaining node in the stack is the root of the expression tree
        return tree_node_stack.pop()  # Correctly return the root of the expression tree

    def evaluate_recursive(self):
        return self._evaluate_recursive(self.root)

    # make _evaluate_recursive() a regular method, not a static method
    def _evaluate_recursive(self, node):
        # base case 
        if isinstance(node.val, int):
            return node.val

        if node.val in '+-*/^':
            left = self._evaluate_recursive(node.left)
            right = self._evaluate_recursive(node.right)

            if node.val == '+':
                return left + right
            elif node.val == '-':
                return left - right
            elif node.val == '*':
                return left * right
            elif node.val == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                return left / right
            elif node.val == '^':
                return left ** right
