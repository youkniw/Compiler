from Token import Token


class Lexer:
    def __init__(self, source, tokenTable1, tokenTable2, dfa):
        self.source = source
        self.tokenTable1 = tokenTable1
        self.tokenTable2 = tokenTable2
        self.dfa = dfa

    def run(self):
        token_now = ""
        text = self.source
        i = 0
        ID = 0
        while i < len(text):
            ch = text[i]
            if token_now == "" and (ch == '\n' or ch == ' ' or ch == '\t'):
                i += 1
                continue

            token_now += ch
            if self.dfa.nextId(ch):
                ID = self.dfa.nowId
                if self.dfa.isFinal(ID):
                    if self.dfa.isBackOff(ID):
                        token_now = token_now[:-1]
                        i -= 1

                    node_tag = self.dfa.getType(ID)
                    token_type = self.dfa.getTokenType(token_now, node_tag)
                    token_num = self.dfa.getTokenNum(token_now, token_type)
                    token_self = self.dfa.getTokenTypeSelf(token_now, node_tag)
                    self.tokenTable1.pushToken(Token(token_now, token_type, token_num))
                    self.tokenTable2.pushToken(Token(token_now, token_self, token_num))
                    token_now = ""
                    self.dfa.getStart()
                i += 1
            else:
                print(ch)
                print("Lexical error: 不符合c--词法！")
                return

        if not self.dfa.isFinal(ID):
            print("Lexical error: 最终一个词不是完整的token")
            return
