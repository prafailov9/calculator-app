from enum import Enum

class Token:
    def __init__(self, token_type, value=None):
        # The type of the token - can be "number", "operator", "variable", or "function"
        self.token_type = token_type

        # The value of the token - for numbers, this will be the numeric value,
        # for operators, this will be the operator symbol, for variables, this will
        # be the variable name, and for functions, this will be the function name.
        self.value = value

class TokenType(Enum):
    NUMBER = 1
    VARIABLE = 2
    OPERATOR = 3
    FUNCTION = 4
    OPEN_PAREN = 5
    CLOSE_PAREN = 6

class Tokenizer:
    def __init__(self, expression):
        self.expression = expression.replace(" ", "")  # Remove all whitespace

    def extract_sequence(self, pos, fn_condition):
        start_pos = pos
        while pos < len(self.expression) and fn_condition(self.expression[pos]):
            pos += 1
        return self.expression[start_pos:pos], pos  # Return new position too

    """
    Break down the expression into a list of Tokens.
    :return: A list of Tokens representing the expression.
    """
    def tokenize(self):
        pos = 0
        tokens = []
        OPERATORS = {'+', '-', '*', '/', '^'}
        PARENTHESIS = {'(', ')'}

        while pos < len(self.expression):
            current_char = self.expression[pos]

            # If the current character is a digit, extract the 
            # whole number and create a NUMBER token.
            if current_char.isdigit():
                number, pos = self.extract_sequence(pos, str.isdigit)
                tokens.append(Token(TokenType.NUMBER, number))

            # If the current character is a letter, extract the 
            # whole alphabetic sequence and create a VARIABLE or FUNCTION token.
            elif current_char.isalpha():
                alpha, pos = self.extract_sequence(pos, str.isalpha)
                if pos < len(self.expression) and self.expression[pos] == '(':
                    tokens.append(Token(TokenType.FUNCTION, alpha))
                else:
                    tokens.append(Token(TokenType.VARIABLE, alpha))

            elif current_char in OPERATORS:
                tokens.append(Token(TokenType.OPERATOR, current_char))
                pos += 1

            elif current_char in PARENTHESIS:
                token_type = TokenType.OPEN_PAREN if current_char == '(' else TokenType.CLOSE_PAREN
                tokens.append(Token(token_type, current_char))
                pos += 1

            elif current_char == ' ':
                pos += 1

            else:
                raise ValueError("Invalid character: '{}'".format(current_char))

        tokens.append(Token(None))

        return tokens
