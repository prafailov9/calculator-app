"""
parser module
"""
from enum import Enum
from ..tokenizer.expression_tokenizer import TokenType
from ..data_structs.stack import Stack


class Precedence(Enum):
    """
    precedence enum
    """
    LOWEST = 1
    ADDSUB = 2
    MULDIV = 3
    POWER = 4
    HIGHEST = 5

# Define the precedence for the operators
OPERATOR_PRECEDENCE = {
    '+': Precedence.ADDSUB,
    '-': Precedence.ADDSUB,
    '*': Precedence.MULDIV,
    '/': Precedence.MULDIV,
    '^': Precedence.POWER
}

class PostfixExpressionParser:
    """
    parser containing logic to convert infix to postfix notation using given tokenizer
    """

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def to_postfix(self):
        """
        Convert an infix expression to a postfix expression.
        :return: A list of Tokens representing the expression in postfix notation.
        """
        output_queue = []
        operator_stack = Stack()

        # Iterate over the tokens
        for token in self.tokenizer.tokenize():
            # If it's a number or a variable, add it to the output queue
            if token.token_type == TokenType.NUMBER or token.token_type == TokenType.VARIABLE:
                output_queue.append(token)

            # If it's an operator, pop operators from the stack to the output if they have
            # higher or equal precedence, then push the current operator to the stack
            elif token.token_type == TokenType.OPERATOR:
                self.parse_operator_tokens(operator_stack, output_queue, token)

            # If it's a function or an open parenthesis, push it to the stack
            elif token.token_type == TokenType.FUNCTION or token.token_type == TokenType.OPEN_PAREN:
                operator_stack.push(token)

            # If it's a close parenthesis, pop from the stack to the output until an
            # open parenthesis is encountered, then discard the open parenthesis
            elif token.token_type == TokenType.CLOSE_PAREN:
                self.parse_parenthesis_tokens(operator_stack, output_queue)

            # End of expression
            elif token.token_type is None:
                break

        # Pop the remaining operators from the stack to the queue
        while not operator_stack.isEmpty():
            if operator_stack.peek().token_type in (TokenType.OPEN_PAREN, TokenType.CLOSE_PAREN):
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())

        return output_queue

    def parse_operator_tokens(self, operator_stack, output_queue, token):
        """
        return: parsed tokens for an operator
        """
        # since postfix expressions are evaluated from left to right, 
        # higher precedence operators are parsed first to maintain correct order of operations.
        while not operator_stack.isEmpty() and \
                operator_stack.peek().token_type == TokenType.OPERATOR and \
                OPERATOR_PRECEDENCE.get(token.value).value <= OPERATOR_PRECEDENCE.get(operator_stack.peek().value).value:
            output_queue.append(operator_stack.pop())
        operator_stack.push(token)

    def parse_parenthesis_tokens(self, operator_stack, output_queue):
        """
        return: parsed tokens in parenthisis
        """
        # while the current operator at the top of the op_stack is 
        # not an open parenthesis - append the operator to the output and remove it from the op_stack
        while not operator_stack.isEmpty() and operator_stack.peek().token_type != TokenType.OPEN_PAREN:
            output_queue.append(operator_stack.pop())
        if operator_stack.isEmpty():
            raise ValueError("Mismatched parentheses")
        operator_stack.pop()  # discard the open parenthesis

        # after appending the parenthesis' subexpression to the output 
        # check if those parenthesis where part of a function
        # then add the function to the output
        if operator_stack.peek().token_type == TokenType.FUNCTION:
            output_queue.append(operator_stack.pop())
