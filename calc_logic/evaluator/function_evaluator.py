import math

class FunctionEvaluator:
    def __init__(self):
        pass
       
    functions = {
        "log": math.log10,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sec": lambda x: 1 / math.cos(x),
        "csc": lambda x: 1 / math.sin(x),
        "cot": lambda x: 1 / math.tan(x)
    }
    
    def eval_function(self, value, func_name):
        # check if the function exists
        if func_name not in self.functions.keys():
            raise ValueError(f"Unsupported function {func_name}")
        return self.functions[func_name](value)