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

    # automatically called when using <= on the Precedence
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented


# Define the precedence for the operators
OPERATOR_PRECEDENCE = {
    '+': Precedence.ADDSUB,
    '-': Precedence.ADDSUB,
    '*': Precedence.MULDIV,
    '/': Precedence.MULDIV,
    '^': Precedence.POWER
}

# RPN parser to convert infix to postfix notation using the shunting yard algorithm.


class PostfixExpressionParser:
    """
    parser containing logic to convert infix to postfix notation using given tokenizer
    """

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def get_operator_precedence(self, operator):
        """return precedence of given operator"""
        return OPERATOR_PRECEDENCE.get(operator, Precedence.LOWEST)

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

            # If it's an operator, pop operators from the stack to the queue if they have
            # higher or equal precedence, then push the current operator to the stack
            elif token.token_type == TokenType.OPERATOR:
                self.parse_operator_tokens(operator_stack, output_queue, token)

            # If it's a function or an open parenthesis, push it to the stack
            elif token.token_type == TokenType.FUNCTION or token.token_type == TokenType.OPEN_PAREN:
                operator_stack.push(token)

            # If it's a close parenthesis, pop from the stack to the queue until an
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

        for token in output_queue:
            print(f"parsed expressing :{token.value}")
        return output_queue

    def parse_operator_tokens(self, operator_stack, output_queue, token):
        """
        return: parsed tokens for an operator
        """
        while not operator_stack.isEmpty() and \
                operator_stack.peek().token_type == TokenType.OPERATOR and \
                self.get_operator_precedence(token.value) <= self.get_operator_precedence(operator_stack.peek().value):
            output_queue.append(operator_stack.pop())
        operator_stack.push(token)

    def parse_parenthesis_tokens(self, operator_stack, output_queue):
        """
        return: parsed tokens in parenthisis
        """
        while not operator_stack.isEmpty() and operator_stack.peek().token_type != TokenType.OPEN_PAREN:
            output_queue.append(operator_stack.pop())
        if operator_stack.isEmpty():
            raise ValueError("Mismatched parentheses")
        operator_stack.pop()  # discard the open parenthesis
