class CustomValidationError(Exception):
    def __init__(self, message="error"):
        self.message = message
        super().__init__(self.message)
