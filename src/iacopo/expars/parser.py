from typing import Iterable

from iacopo.expars import (
    Token,
    Operation,
    Number,
    Operator,
    OperatorToken,
    OpenParenthesis,
    ClosedParenthesis,
    Evaluable,
    ParenthesisOperation,
)
from iacopo.expars.exceptions import UnexpectedTokenError, IncompleteExpressionError
from iacopo.expars.utils import PeekIterator


class Parser:
    def __init__(self, tokens: Iterable[Token], inside_parenthesis=False):
        self._tokens = PeekIterator(tokens)
        self._current_token = None
        self._shift()
        self._inside_parenthesis = inside_parenthesis

    def parse(self) -> Evaluable:
        self._process_negative_number()
        self._parse_checks()
        left = self._current_token
        if isinstance(left, OpenParenthesis):
            left = self._parse_parenthesis()

        if not self._tokens.has_next():
            return left

        return self._complete_expression(left)

    def _parse_parenthesis(self):
        inner_parser = Parser(self._tokens, inside_parenthesis=True)
        left = inner_parser.parse()
        self._tokens = inner_parser._tokens
        return left

    def _parse_checks(self):
        if isinstance(self._current_token, OperatorToken):
            # expression cannot start with a token
            raise UnexpectedTokenError(self._current_token)
        # now current_token is a number
        assert isinstance(self._current_token, (Number, OpenParenthesis))
        # we need either zero or more than one token after a number or a parenthesis
        if self._tokens.has_next():
            next_ = self._tokens.peek(0)
            try:
                self._tokens.peek(1)
            except StopIteration:
                if isinstance(next_, ClosedParenthesis):
                    if self._inside_parenthesis:
                        return
                    else:
                        raise UnexpectedTokenError(next_)

                raise IncompleteExpressionError(next_)

    def _shift(self):
        self._current_token = next(self._tokens)
        return self._current_token

    def _process_negative_number(self):
        if (
            self._tokens.has_next()
            and self._is_minus(self._current_token)
            and isinstance(self._tokens.peek(), Number)
        ):
            position = self._current_token.position
            self._shift()
            self._current_token.value = -self._current_token.value
            self._current_token.position = position

    def _complete_expression(self, left) -> Evaluable:
        match self._shift():
            case ClosedParenthesis() as closed:
                if self._inside_parenthesis:
                    return left
                raise UnexpectedTokenError(closed)
            case OperatorToken() as operator_token:
                self._shift()
                right = self.parse()
                return self._build_operation(operator_token.operator, left, right)
            case _ as unexpected:
                raise UnexpectedTokenError(unexpected)

    @classmethod
    def _is_minus(cls, token):
        return isinstance(token, OperatorToken) and token.operator == Operator.MINUS

    def _build_operation(
        self,
        operator: Operator,
        left: Evaluable,
        right: Evaluable,
    ):
        operation_class = (
            ParenthesisOperation if self._inside_parenthesis else Operation
        )
        ret = operation_class(operator, left, right)
        if ret.has_precedence_over(right):
            # the evaluation is performed depth-first, so if the right is a low-priority operation
            # we must change the tree structure in order to have the left branch evaluated before
            high_priority_operation = Operation(operator, left, right.left)
            right.left = high_priority_operation
            ret = right
        return ret
