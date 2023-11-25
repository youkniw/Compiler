class TextParseInput:
    lex_result_stack = []

    @staticmethod
    def setLex_result_stack(lex):
        TextParseInput.lex_result_stack = lex
