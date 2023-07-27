# Utility functions for the calculation service
import math

def is_operator(operator):
    return True if operator in ('+', '-', '*', '/', '^') else False

def determine_operator_precedence(operator):
    if operator == '^': return 3
    elif operator in ('*', '/'): return 2
    elif operator in ('+', '-'): return 1
    else:
        raise Exception("Invalid operator {}!".format(operator))
    
import math

def is_function(function):
    return function in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh']

def evaluate_function(function, value):
    if function == 'sin':
        return math.sin(value)
    elif function == 'cos':
        return math.cos(value)
    elif function == 'tan':
        return math.tan(value)
    elif function == 'asin':
        return math.asin(value)
    elif function == 'acos':
        return math.acos(value)
    elif function == 'atan':
        return math.atan(value)
    elif function == 'sinh':
        return math.sinh(value)
    elif function == 'cosh':
        return math.cosh(value)
    elif function == 'tanh':
        return math.tanh(value)
    elif function == 'asinh':
        return math.asinh(value)
    elif function == 'acosh':
        return math.acosh(value)
    elif function == 'atanh':
        return math.atanh(value)
    else:
        raise Exception("Invalid function {}!".format(function))
