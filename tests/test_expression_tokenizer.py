import unittest
from calc_logic.tokenizer.expression_tokenizer import Tokenizer, TokenType

class TestExpressionTokenizer(unittest.TestCase):
    def test_numbers(self):
        tokenizer = Tokenizer("123")
        tokens = tokenizer.tokenize()
        self.assertEqual(tokens[0].token_type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, "123")

    def test_variables(self):
        tokenizer = Tokenizer("x")
        tokens = tokenizer.tokenize()
        self.assertEqual(tokens[0].token_type, TokenType.VARIABLE)
        self.assertEqual(tokens[0].value, "x")

    def test_operators(self):
        tokenizer = Tokenizer("+")
        tokens = tokenizer.tokenize()
        self.assertEqual(tokens[0].token_type, TokenType.OPERATOR)
        self.assertEqual(tokens[0].value, "+")

    def test_functions(self):
        tokenizer = Tokenizer("sin(")
        tokens = tokenizer.tokenize()
        self.assertEqual(tokens[0].token_type, TokenType.FUNCTION)
        self.assertEqual(tokens[0].value, "sin")
        self.assertEqual(tokens[1].token_type, TokenType.OPEN_PAREN)

    def test_parentheses(self):
        tokenizer = Tokenizer("()")
        tokens = tokenizer.tokenize()
        self.assertEqual(tokens[0].token_type, TokenType.OPEN_PAREN)
        self.assertEqual(tokens[1].token_type, TokenType.CLOSE_PAREN)

    def test_unknown(self):
        tokenizer = Tokenizer("@")
        with self.assertRaises(ValueError):
            tokenizer.tokenize()
        

    def test_complex_expr(self):
        tokenizer = Tokenizer("1+22/4*((11-2)+sin(x))")
        tokens = tokenizer.tokenize()
        self.assertEqual(tokens[0].value, "1"), self.assertEqual(tokens[0].token_type, TokenType.NUMBER),
        self.assertEqual(tokens[1].value, "+"), self.assertEqual(tokens[1].token_type, TokenType.OPERATOR),
        self.assertEqual(tokens[2].value, "22"), self.assertEqual(tokens[2].token_type, TokenType.NUMBER),
        self.assertEqual(tokens[3].value, "/"), self.assertEqual(tokens[3].token_type, TokenType.OPERATOR),
        self.assertEqual(tokens[4].value, "4"), self.assertEqual(tokens[4].token_type, TokenType.NUMBER),
        self.assertEqual(tokens[5].value, "*"), self.assertEqual(tokens[5].token_type, TokenType.OPERATOR),
        self.assertEqual(tokens[6].value, "("), self.assertEqual(tokens[6].token_type, TokenType.OPEN_PAREN),
        self.assertEqual(tokens[7].value, "("), self.assertEqual(tokens[7].token_type, TokenType.OPEN_PAREN),
        self.assertEqual(tokens[8].value, "11"), self.assertEqual(tokens[8].token_type, TokenType.NUMBER),
        self.assertEqual(tokens[9].value, "-"), self.assertEqual(tokens[9].token_type, TokenType.OPERATOR),
        self.assertEqual(tokens[10].value, "2"), self.assertEqual(tokens[10].token_type, TokenType.NUMBER),
        self.assertEqual(tokens[11].value, ")"), self.assertEqual(tokens[11].token_type, TokenType.CLOSE_PAREN),
        self.assertEqual(tokens[12].value, "+"), self.assertEqual(tokens[12].token_type, TokenType.OPERATOR),
        self.assertEqual(tokens[13].value, "sin"), self.assertEqual(tokens[13].token_type, TokenType.FUNCTION),
        self.assertEqual(tokens[14].value, "("), self.assertEqual(tokens[14].token_type, TokenType.OPEN_PAREN),
        self.assertEqual(tokens[15].value, "x"), self.assertEqual(tokens[15].token_type, TokenType.VARIABLE),
        self.assertEqual(tokens[16].value, ")"), self.assertEqual(tokens[16].token_type, TokenType.CLOSE_PAREN),
        self.assertEqual(tokens[17].value, ")"), self.assertEqual(tokens[17].token_type, TokenType.CLOSE_PAREN),
        
if __name__ == '__main__':
    unittest.main()