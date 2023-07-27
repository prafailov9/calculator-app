from calc_logic.data_structs.stack import Stack
from .. import calculation_utils

class ExpressionNode :
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class ExpressionTree:
    #variables is an optional param
    def __init__(self, postfix_expr, variables = None):
        if variables is None:
            variables = {}
        self.variables = variables
        self.root = self.build_tree(postfix_expr)

    @staticmethod
    def build_tree(postfix_expr):
        print("1. start building the tree...\n")
        tree_node_stack = Stack()

        for current in postfix_expr.split():
            if current in ('+', '-', '*', '/', '^'):
                # Create a new node for the operator
                node = ExpressionNode(current)

                # Pop two nodes and make them children of the new node
                node.right = tree_node_stack.pop() if not tree_node_stack.isEmpty() else None
                node.left = tree_node_stack.pop() if not tree_node_stack.isEmpty() else None
                print("2. created operator node with its operands {}, {}...\n".format(node.right.value, node.left.value))
                # if the stack was empty and node.left or node.right is None, then raise an error
                if node.left is None or node.right is None:
                    raise ValueError("The expression is not well formed. Not enough operands for the operators.")
            
            elif calculation_utils.is_function(current):
                node = ExpressionNode(current)
                node.right = tree_node_stack.pop() if not tree_node_stack.isEmpty() else None
                print("2. created function node with its operand {},...\n".format(node.right.value))
                if node.right is None:
                    raise ValueError("The expression is not well formed. Not enough operands for the functions.")
            
            else:
                # Create a new node for the number/variable and push it to the stack
                node = ExpressionNode(current)

            tree_node_stack.push(node)

        # The remaining node in the stack is the root of the expression tree
        print("3. the rroot node is {}\n".format(tree_node_stack.peek().value))
        return tree_node_stack.pop()  # Correctly return the root of the expression tree

    def evaluate_recursive(self, node):
        # base case 
        if isinstance(node.value, int):
            return node.value

        # Check if the string can be converted to a number
        try:
            return float(node.value)
        except ValueError:
            # If not, it should be a variable
            if not calculation_utils.is_operator(node.value):
                if node.value in self.variables:
                    print(f"Replacing variable {node.value} with value {self.variables[node.value]}")
                    return self.variables[node.value]
                else:
                    print(f"Variable {node.value} not found in variables: {self.variables}")


        # continue with operator logic
        if calculation_utils.is_operator(node.value):
            left = self.evaluate_recursive(node.left)
            right = self.evaluate_recursive(node.right)

            # Add a print statement here too, to see what's going on
            print(f"Calculating: {left} {node.value} {right}")
            if node.value == '+':
                return left + right
            elif node.value == '-':
                return left - right
            elif node.value == '*':
                return left * right
            elif node.value == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                return left / right
            elif node.value == '^':
                return left ** right
