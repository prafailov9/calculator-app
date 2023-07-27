from calc_logic.evaluator.postfix_expression_evaluator import ExpressionTree
from calc_logic.tokenizer.expression_tokenizer import Tokenizer, TokenType
from calc_logic.parser.postfix_expression_parser import PostfixExpressionParser
import pytest
import math

"1+22/4*((11-2)+sin(2))"

def test_simple_expression_tree():
    result = parse_and_eval("2 + 2")
    assert result == 4.0

def test_expression_tree_with_parentheses():
    result = parse_and_eval("2 * (2 + 2)")
    assert result == 8.0

def test_expression_tree_with_powers():
    result = parse_and_eval("2 ^ 3 ^ 2")
    assert result == 512.0

def test_expression_tree_with_functions():
    result = parse_and_eval("sin(0)")
    assert math.isclose(result, 0.0)

def test_expression_tree_with_complex_expression():
    result = parse_and_eval("1+22/4*((11-2)+tan(2))+3^3")
    assert result == 65.48228075206165

def test_expression_tree_invalid_token():
    with pytest.raises(ValueError):
       parse_and_eval("2 ? 2")
    
def parse_and_eval(expr):
    postfix = PostfixExpressionParser(Tokenizer(expr)).to_postfix()
    expr_tree = ExpressionTree(postfix)
    return expr_tree.evaluate()
    