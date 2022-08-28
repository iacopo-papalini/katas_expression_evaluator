from __future__ import annotations

from abc import ABC
from typing import Tuple, Iterable

from iacopo.expars import (
    Token,
    CharacterParser,
    Symbol,
    Operator,
    Digit,
    Dot,
    Number,
    OperatorToken,
    OpenParenthesis,
    ClosedParenthesis,
)
from iacopo.expars.exceptions import NumberFormatError, UnexpectedTokenError


class Status(ABC):
    def analyse(
        self, symbol: Symbol, position: int
    ) -> Tuple[Token | None, Status | None, bool]:
        raise NotImplementedError()


class BaseStatus(Status):
    def analyse(
        self, symbol: Symbol, position: int
    ) -> Tuple[Token | None, Status | None, bool]:
        match symbol:
            case Operator():
                return OperatorToken(Operator(symbol.value), position), self, True
            case Digit() | Dot():
                return None, NumberParsingStatus(symbol.value), True
            case ClosedParenthesis() | OpenParenthesis() as parenthesis:
                parenthesis.position = position
                return parenthesis, self, True

    def finalize(self, position) -> Token | None:
        return None


class NumberParsingStatus(Status):
    def __init__(self, first_value):
        self.accumulator = first_value

    def analyse(
        self, symbol: Symbol, position: int
    ) -> Tuple[Token | None, Status | None, bool]:
        match symbol:
            case Digit():
                self.accumulator += symbol.value
                return None, self, True
            case Dot():
                if "." in self.accumulator:
                    raise NumberFormatError(position, "Unexpected '.'")
                self.accumulator += symbol.value
                return None, self, True
            case Operator() | ClosedParenthesis():
                return self.finalize(position), BaseStatus(), False
            case OpenParenthesis() as open_parenthesis:
                open_parenthesis.position = position
                raise UnexpectedTokenError(open_parenthesis)

    def finalize(self, position) -> Token | None:
        return Number(float(self.accumulator), position)


class Tokenizer:
    def __init__(self, expression: str):
        self.expression = expression

    def tokenize(self) -> Iterable[Token]:
        current_status = BaseStatus()
        for position, char in enumerate(self.expression):
            symbol = CharacterParser.parse_char(char)
            processed = False
            while not processed:
                token, current_status, processed = current_status.analyse(
                    symbol, position + 1
                )
                if token:
                    yield token

        if current_status:
            last = current_status.finalize(len(self.expression))
            if last is not None:
                yield last
