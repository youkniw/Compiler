class Token:
    def __init__(self, lexeme, tokenType, tokenNum):
        self.lexeme = lexeme
        self.tokenType = tokenType
        self.tokenNum = tokenNum

    def getLexeme(self):
        return self.lexeme

    def getTokenType(self):
        return self.tokenType

    def getTokenNum(self):
        return self.tokenNum
