class TokenTable:
    def __init__(self):
        self.tokens = []

    def printTokenTable(self):
        for token in self.tokens:
            print(f"{token.getLexeme()}   <{token.getTokenType()},{token.getTokenNum()}>")

    def pushToken(self, token):
        self.tokens.append(token)

    def saveTokenTable(self, path):
        try:
            with open(path, 'w') as f:
                for i, token in enumerate(self.tokens):
                    if i != len(self.tokens) - 1:
                        f.write(f"{token.getLexeme()}   <{token.getTokenType()},{token.getTokenNum()}>\n")
                    else:
                        f.write(f"{token.getLexeme()}   <{token.getTokenType()},{token.getTokenNum()}>")
        except Exception as e:
            print(e)
        return enumerate(self.tokens)
