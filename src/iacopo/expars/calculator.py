from iacopo.expars.parser import Parser
from iacopo.expars.tokenizer import Tokenizer


class Calculator:
    def calculate(self, expression: str) -> float:
        tokenizer = Tokenizer(expression)
        return Parser(tokenizer.tokenize()).parse().evaluate()
