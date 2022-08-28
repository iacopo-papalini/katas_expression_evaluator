from __future__ import annotations
from enum import Enum

from pydantic import BaseModel, Field


class Token:
    def __init__(self, position: int):
        self.position = position


class Evaluable:
    def evaluate(self) -> float:
        raise NotImplementedError()

    def precedence(self):
        raise NotImplementedError()


class Symbol:
    @property
    def value(self) -> str:
        raise NotImplementedError()


class Number(Token, Evaluable):
    value: float

    def __init__(self, value, position=0):
        super().__init__(position=position)
        self.value = value

    def evaluate(self) -> float:
        return float(self.value)

    def __repr__(self):
        return f"Number {self.value}"

    def precedence(self):
        return 0


class OpenParenthesis(Symbol, Token):
    def __init__(self, position=0):
        super().__init__(position=position)

    @property
    def value(self) -> str:
        return "("

    def __repr__(self):
        return self.value


class ClosedParenthesis(Symbol, Token):
    def __init__(self, position=0):
        super().__init__(position=position)

    @property
    def value(self) -> str:
        return ")"

    def __repr__(self):
        return self.value


class Digit(BaseModel, Symbol):
    digit: int = Field(ge=0, le=9)

    @property
    def value(self):
        return str(self.digit)


class Dot(Symbol):
    def __init__(self, *_):
        pass

    @property
    def value(self):
        return "."


class Operator(Symbol, Enum):
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"

    @property
    def value(self) -> str:
        return self._value_

    @classmethod
    def precedence(cls, operator: Operator):
        match operator:
            case Operator.PLUS | Operator.MINUS:
                return 3
            case Operator.DIVIDE | Operator.MULTIPLY:
                return 2


class OperatorToken(Token):
    def __init__(self, operator: Operator, position):
        super().__init__(position=position)
        self.operator = operator

    def __repr__(self):
        return f"{self.operator}"


class Operation(Evaluable):
    def __init__(self, operator: Operator, left: Evaluable, right: Evaluable):
        self.operator = operator
        self.left = left
        self.right = right

    def evaluate(self) -> float:
        left = self.left.evaluate()
        right = self.right.evaluate()
        match self.operator:
            case Operator.PLUS:
                return left + right
            case Operator.MINUS:
                return left - right
            case Operator.DIVIDE:
                return left / right
            case Operator.MULTIPLY:
                return left * right

    def as_polish(self):
        left = (
            self.left.value if isinstance(self.left, Number) else self.left.as_polish()
        )
        right = (
            self.right.value
            if isinstance(self.right, Number)
            else self.right.as_polish()
        )
        return f"{left} {right} {self.operator.value}"

    def precedence(self):
        return Operator.precedence(self.operator)

    def has_precedence_over(self, other_operation):
        if not isinstance(other_operation, Operation):
            return False
        # 0 means max precedence
        return self.precedence() < other_operation.precedence()


class ParenthesisOperation(Operation):
    def precedence(self):
        return 0


class CharacterParser:
    @staticmethod
    def parse_char(char) -> Symbol:
        match char:
            case "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "0":
                return Digit(digit=int(char))
            case "+" | "-" | "*" | "/":
                return Operator(char)
            case ".":
                return Dot()
            case "(":
                return OpenParenthesis()
            case ")":
                return ClosedParenthesis()
