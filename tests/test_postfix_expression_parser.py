import unittest
from calc_logic.tokenizer.expression_tokenizer import Tokenizer, TokenType
from calc_logic.parser.postfix_expression_parser import PostfixExpressionParser, Precedence

class TestPostfixExpressionParser(unittest.TestCase):
    def setUp(self):
        self.parser = None

    def test_basic_expression(self):
        self.parser = PostfixExpressionParser(Tokenizer("2+2"))
        result = self.parser.to_postfix()
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].value, "2")
        self.assertEqual(result[0].token_type, TokenType.NUMBER)
        self.assertEqual(result[1].value, "2")
        self.assertEqual(result[1].token_type, TokenType.NUMBER)
        self.assertEqual(result[2].value, "+")
        self.assertEqual(result[2].token_type, TokenType.OPERATOR)

    def test_operator_precedence(self):
        self.parser = PostfixExpressionParser(Tokenizer("2+2*2"))
        result = self.parser.to_postfix()
        self.assertEqual(len(result), 5)
        self.assertEqual(result[4].value, "+")
        self.assertEqual(result[4].token_type, TokenType.OPERATOR)

    def test_parentheses(self):
        self.parser = PostfixExpressionParser(Tokenizer("(2+2)*2"))
        result = self.parser.to_postfix()
        self.assertEqual(len(result), 5)
        self.assertEqual(result[4].value, "*")
        self.assertEqual(result[4].token_type, TokenType.OPERATOR)

    def test_function(self):
        self.parser = PostfixExpressionParser(Tokenizer("sin(2)"))
        result = self.parser.to_postfix()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].value, "2")
        self.assertEqual(result[0].token_type, TokenType.NUMBER)
        self.assertEqual(result[1].value, "sin")
        self.assertEqual(result[1].token_type, TokenType.FUNCTION)

    def test_mismatched_parentheses(self):
        self.parser = PostfixExpressionParser(Tokenizer("(2+2"))
        with self.assertRaises(ValueError):
            self.parser.to_postfix()

        self.parser = PostfixExpressionParser(Tokenizer("2+2)"))
        with self.assertRaises(ValueError):
            self.parser.to_postfix()

    def test_invalid_character(self):
        self.parser = PostfixExpressionParser(Tokenizer("2+2$"))
        with self.assertRaises(ValueError):
            self.parser.to_postfix()

if __name__ == "__main__":
    unittest.main()
