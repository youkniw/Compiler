"""from Config import Config


class TextLexiconInput:
    @staticmethod
    def input():
        path = Config.lexInputPath
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except IOError as e:
            raise RuntimeError(e)
"""