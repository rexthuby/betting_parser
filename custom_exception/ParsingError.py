class ParsingError(Exception):
    def __init__(self, message='Parsing error'):
        self.message = message
        super().__init__(self.message)