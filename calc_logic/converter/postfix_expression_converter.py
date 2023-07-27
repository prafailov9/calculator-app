from data_structs.stack import Stack

class PostfixExpressionConverter:
    def __init__(self, operatorStack = Stack()):
        self.operatorStack = operatorStack

    def isOperator(self, character):
        return True if character in ('+', '-', '*', '/', '^') else False
    
    def determine_operator_precedence(self, operator):
        if operator == '^': return 3
        elif operator in ('*', '/'): return 2
        elif operator in ('+', '-'): return 1
        else:
            raise Exception("Invalid operator {}!".format(operator))

    #convert a given infix expression into postfix notation. 
    # If the character is a digit, add it in a buffer (num_buffer) to handle multi-digit numbers. 
    # If an operator or parentheses is encountered, it adds the number collected so far 
    # to the output and handles the operator/parentheses according to the standard infix 
    # to postfix conversion rules. At the end, it flushes any remaining operators from the 
    # operator stack to the output. 
    # The result is a string of space-separated numbers and operators in postfix notation.
    def convert(self, expression):
        output = []
        num_buffer = []
        
        for i in range(len(expression)):
            current = expression[i]

            # Skip spaces
            if current == ' ':
                continue

            # If the current character is a digit, add it to the buffer
            if current.isdigit():
               num_buffer.append(current)
            
            # If the current character is not a digit, add the buffer to the output
            # and clear the buffer for the next number
            else:
                if num_buffer:
                    output.append(''.join(num_buffer))
                    num_buffer = []
            
            if self.isOperator(current):
                operator = current
                while (not self.operatorStack.isEmpty() and 
                       self.isOperator(self.operatorStack.peek()) and 
                       self.determine_operator_precedence(self.operatorStack.peek()) >= self.determine_operator_precedence(operator)):
                    output.append(self.operatorStack.pop())
                self.operatorStack.push(operator)
            
            if current == '(': 
                self.operatorStack.push(current)
            
            if current == ')': 
                while self.operatorStack.peek() != '(':
                    output.append(self.operatorStack.pop())
                self.operatorStack.pop()
        
        # If there are any leftover digits in the buffer, add them to the output
        if num_buffer:
            output.append(''.join(num_buffer))
        
        while not self.operatorStack.isEmpty():
            output.append(self.operatorStack.pop())
        
        return ' '.join(output)
