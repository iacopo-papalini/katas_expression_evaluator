class NumberFormatError(RuntimeError):
    def __init__(self, position, message):
        super().__init__(f"{message} at character {position}")
        self.message = message
        self.position = position


class UnexpectedTokenError(RuntimeError):
    def __init__(self, token):
        super().__init__(f"Unexpected token '{token}' at character {token.position}")
        self.position = token.position


class IncompleteExpressionError(RuntimeError):
    def __init__(self, token):
        super().__init__(
            f"Missing symbol at the end of expression, last token parsed: {token} at position {token.position}"
        )
