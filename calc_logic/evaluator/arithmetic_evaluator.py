import operator

class ArithmeticEvaluator:
    def __init__(self):
        pass

    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "^": operator.pow,
    }
        
    def eval_expression(self, val1, val2, op):
        return self.operators[op](val1, val2)

