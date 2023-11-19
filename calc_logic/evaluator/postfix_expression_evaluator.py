from calc_logic.tokenizer.expression_tokenizer import TokenType
from calc_logic.data_structs.stack import Stack
from calc_logic.evaluator.function_evaluator import FunctionEvaluator
from calc_logic.evaluator.arithmetic_evaluator import ArithmeticEvaluator

trig_evaluator = FunctionEvaluator()
arith_evaluator = ArithmeticEvaluator()

class ExpressionNode:
    def __init__(self, token_type, value, left=None, right=None):
        self.token_type = token_type 
        self.value = value
        self.left = left
        self.right = right

    def evaluate(self):
        if self.token_type == TokenType.NUMBER:
            return float(self.value)
        elif self.token_type == TokenType.VARIABLE:
            raise ValueError("Variables not supported in evaluation")
        elif self.token_type == TokenType.OPERATOR:
            return arith_evaluator.eval_expression(self.left.evaluate(), self.right.evaluate(), self.value)
        elif self.token_type == TokenType.FUNCTION:
            return trig_evaluator.eval_function(self.right.evaluate(), self.value)          

class ExpressionTree:
    def __init__(self, postfix_tokens):
        self.root = self.build_tree(postfix_tokens)

    def build_tree(self, postfix_tokens):
        print("Building tree for postfix expression: ")
        print(' '.join(str(x.value) for x in postfix_tokens))

        stack = Stack()
        for token in postfix_tokens:
            if token.token_type in (TokenType.NUMBER, TokenType.VARIABLE):
                stack.push(ExpressionNode(token.token_type, token.value))
            elif token.token_type in (TokenType.OPERATOR, TokenType.FUNCTION):
                right_node = stack.pop()
                if token.token_type == TokenType.OPERATOR:
                    left_node = stack.pop()
                else:  # for function there is only one operand
                    left_node = None
                
                stack.push(ExpressionNode(token.token_type, token.value, left_node, right_node))
            else:
                raise ValueError(f"Invalid token {token.value}")
            
        return stack.pop()

    def evaluate(self):
        return self.root.evaluate()
    