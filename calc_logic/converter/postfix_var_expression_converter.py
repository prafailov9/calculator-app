from calc_logic.data_structs.stack import Stack
from .. import calculation_utils

class PostfixExpressionConverter:
    def __init__(self, operatorStack = Stack()):
        self.operatorStack = operatorStack

    def convert(self, expression):
        print("starting convertion...\n")
        output = []
        num_buffer = [] 
        var_buffer = []

        valid_functions = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh']
        
        for i in range(len(expression)):
            current = expression[i]

            # Skip spaces
            if current == ' ':
                continue

            # If the current character is a digit, add it to the num_buffer
            if current.isdigit():
               num_buffer.append(current)
            
            # If the current character is an alphanumeric character but not a digit, 
            # add it to the var_buffer
            elif current.isalpha():
               var_buffer.append(current)
               if ''.join(var_buffer) in valid_functions:
                   output.append(''.join(var_buffer))
                   var_buffer = []

            # If the current character is not a digit or an alphanumeric character, 
            # add the num_buffer or var_buffer to the output
            # and clear the buffers for the next number/variable
            else:
                if num_buffer:
                    output.append(''.join(num_buffer))
                    num_buffer = []
                elif var_buffer:
                    output.append(''.join(var_buffer))
                    var_buffer = []
            print("checking for operator...\n")
            if calculation_utils.is_operator(current):
                print("in operator check block...\n")
                self.append_operators_to_output(current, output)
            
            if current == '(': 
                self.operatorStack.push(current)
            
            if current == ')': 
                while self.operatorStack.peek() != '(':
                    output.append(self.operatorStack.pop())
                self.operatorStack.pop()
        
        # If there are any leftover digits or variable characters in the buffer, 
        # add them to the output
        if num_buffer:
            output.append(''.join(num_buffer))
        elif var_buffer:
            output.append(''.join(var_buffer))
        
        while not self.operatorStack.isEmpty():
            output.append(self.operatorStack.pop())
        
        print("successfully built output string: {}".format(output))
        return ' '.join(output)

    # when the current char is an operator,
    # append the highest precedence operators to the output string 
    # util no operators are left in the stack
    def append_operators_to_output(self, operator, output):
        print("appending operators to output string...\n")
        while (not self.operatorStack.isEmpty() and 
            calculation_utils.is_operator(self.operatorStack.peek()) and 
            calculation_utils.determine_operator_precedence(self.operatorStack.peek()) >= calculation_utils.determine_operator_precedence(operator)):
            output.append(self.operatorStack.pop())
        self.operatorStack.push(operator)
        print("appending ops success...\n")
