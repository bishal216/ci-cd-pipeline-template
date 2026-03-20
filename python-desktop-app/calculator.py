class Calculator:
    def __init__(self):
        self.expression = ""
        self.reset_next = False

    def append(self, value: str) -> str:
        if self.reset_next and value[0] not in "+-*/":
            self.expression = ""
            self.reset_next = False
        self.expression += value
        return self.expression

    def evaluate(self) -> str:
        try:
            result = str(eval(self.expression))  # noqa: S307
            self.expression = result
            self.reset_next = True
            return result
        except ZeroDivisionError:
            self.expression = ""
            return "div/0"
        except Exception:
            self.expression = ""
            return "error"

    def clear(self) -> str:
        self.expression = ""
        self.reset_next = False
        return "0"

    def backspace(self) -> str:
        self.expression = self.expression[:-1]
        return self.expression or "0"
