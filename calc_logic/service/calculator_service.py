import numpy as np

from calc_logic.tokenizer.expression_tokenizer import Tokenizer, Token, TokenType
from calc_logic.parser.postfix_expression_parser import PostfixExpressionParser
from calc_logic.evaluator.postfix_expression_evaluator import ExpressionTree

class CalculatorService:
    
    def __init__(self):
        pass
    
    def calculate_expression(self, expression):
        # Convert the infix expression to postfix
        parser = PostfixExpressionParser(Tokenizer(expression))
        postfix_expression = parser.to_postfix()
        
        # Build the expression tree and calculate the result
        tree = ExpressionTree(postfix_expression)
        result = tree.evaluate()
        print(f"result is = {result}")
        return result
    
    def calculate_graph(self, func_expression, range_start, range_end, steps):
        try:
            parser = PostfixExpressionParser(Tokenizer(func_expression))
            postfix_expression = parser.to_postfix()  
            #Return evenly spaced numbers over a specified interval.
            x_values = np.linspace(range_start, range_end, steps)
            results = []
            
            # Calculate the result for each x value
            for x in x_values:
                postfix_expression_for_x = self.substitute_variable(postfix_expression, x)
                tree = ExpressionTree(postfix_expression_for_x)
                results.append(tree.evaluate())
                
            # Combine x_values and results into pairs for the graph
            data_pairs = list(zip(x_values.tolist(), results))

            return data_pairs

        except Exception as e:
            raise ValueError("Error processing graph calculation: " + str(e))
    
    def substitute_variable(self, postfix_tokens, x):
        new_tokens = []
        for token in postfix_tokens:
            if token.token_type == TokenType.VARIABLE:
                new_token = Token(TokenType.NUMBER, x)
                new_tokens.append(new_token)
            else:
                new_tokens.append(token)
        return new_tokens

