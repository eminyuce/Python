# exceptions.py
class InvalidInputError(ValueError):
    def __init__(self, message, invalid_value):
        super().__init__(message)
        self.invalid_value = invalid_value

    def __str__(self):
        return f"{self.message}. Invalid value: {self.invalid_value}"