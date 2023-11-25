
"""
class TextLexicon:
    def __init__(self, text):
        self.text = text
        self.text_length = len(text)
        self.row_number = 1
        self.threeElements = []
        self.lex_result_stack = []
        self.lex_error_stack = []

        self.Key = ["void", "int", "long", "double", "char", "float", "else", "if",
                    "return", "for", "goto", "short", "static", "while", "do", "main", "const"]
"""

"""    
    def get_Lex_Result(self):
        return self.lex_result_stack

    def get_Lex_Error(self):
        return self.lex_error_stack

    def getThreeElements(self):
        return self.threeElements

    def isAlpha(self, c):
        if (c.isalpha() or c == '_'):
            return 1
        else:
            return 0

    def isNumber(self, c):
        if (c.isdigit()):
            return 1
        else:
            return 0

    def isKey(self, t):
        if (t in self.Key):
            return 1
        else:
            return 0
"""
"""
    def scanner_all(self):
        i = 0
        # Python 中不需要特意添加 '\0'，因为字符串索引越界会自动抛出异常
        while i < self.text_length:
            c = self.text[i]
            if c in [' ', '\t']:
                i += 1
            elif c in ['\r', '\n']:
                self.row_number += 1
                i += 1
            else:
                i = self.scannerPart(i)

    def scannerPart(self, arg0):
        i = arg0
        ch = self.text[i]
        s = ch

        if self.isAlpha(ch):
            return self.handle_first_alpha(i, s)
        elif self.isNumber(ch):
            return self.handleFirstNum(i, s)
        else:
            if ch in [' ', '\n', '\r', '\t']:
                return i + 1
            elif ch in ['[', ']', '(', ')', '{', '}']:
                self.printResult(s, "双界符")
                return i + 1
            elif ch in [':']:
                if self.text[i + 1] == '=':
                    s = s + '=';
                    self.printResult(s, "界符")
                    return i + 2
                else:
                    self.printError(self.row_number, s, "不能识别")
                    return i + 1
            elif ch in [',', '.', ';']:
                self.printResult(s, "单界符")
                i = i + 1
                return i
            elif ch in ['\\']:
                next_char = self.text[i + 1] if i + 1 < len(self.text) else ''
                if next_char in ['n', 't', 'r']:
                    s += next_char
                    self.printResult(s, "转义")
                    return i + 2
            elif ch in ['\'']:
                return self.handleChar(i, s)
            elif ch in ['+']:

                return self.handlePlus(i, s)
            elif ch in ['-']:
                return self.handleMinus(i, s)
            elif ch in ['*', '/']:

                if (self.text[i + 1] == '*'):
                    return self.handleNote(i, s)
                elif (self.text[i + 1] == '/'):
                    return self.handleSingleLineNote(i, s)
            if ch in ['!', '=']:
                if i + 1 < len(self.text) and self.text[i + 1] == '=':
                    s += self.text[i + 1]
                    self.printResult(s, "运算符")
                    return i + 2
                else:
                    self.printResult(s, "运算符")
                    return i + 1
            elif ch == '>':
                return self.handleMore(i, s)
            elif ch == '<':
                return self.handleLess(i, s)
            elif ch == '%':
                if i + 1 < len(self.text) and self.text[i + 1] in ['=', 's', 'c', 'd', 'f', 'l']:
                    s += self.text[i + 1]
                    type_label = "输出类型标识符" if self.text[i + 1] != '=' else "运算符"
                    self.printResult(s, type_label)
                    return i + 2
                else:
                    self.printResult(s, "求余标识符")
                    return i + 1
            self.printError(self.row_number, s, "暂时无法识别的标识符")
            return i + 1

    def handleFirstAlpha(self, arg, arg0):
        i = arg
        s = arg0
        while i < len(self.text) and (self.isAlpha(self.text[i]) or self.isNumber(self.text[i])):
            s += self.text[i]
            i += 1

        if self.is_key(s):
            self.printResult(s, "关键字")
        else:
            self.printResult(s, "标识符")
        return i

    def handleFirstNum(self, arg, arg0):
        i = arg
        s = arg0
        ch = self.text[i] if (i) < len(self.text) else ''
        i = i + 1
        while i < len(self.text) and self.isNumber(ch):
            s += ch
            i += 1
            ch = self.text[i] if i < len(self.text) else ''

        # ... 处理不同的数值类型（整数、浮点数、科学计数法等）

        if i < self.text_length:
            next_char = self.text[i]
            if next_char in [' ', '\t', '\n', '\r', '\0', ';', ',', ')', ']', '[', '(']:
                self.print_result(s, "整数")
                return i

        elif ch == 'E':
            if i + 1 < self.text_length and self.text[i + 1] == '+':
                s += ch
                i += 1
                ch = self.text[i]
                s += ch
                i += 1
                ch = self.text[i] if i < self.text_length else ''
                while i < self.text_length and self.isNumber(ch):
                    s += ch
                    i += 1
                    ch = self.text[i] if i < self.text_length else ''

                if ch in ['\r', '\n', ';', '\t']:
                    self.printResult(s, "科学计数")
                    return i
                else:
                    self.printError(self.row_number, s, "浮点数错误")
                    return i
            elif self.isNumber(self.text[i + 1]):
                s += ch
                i += 1
                ch = self.text[i] if i < len(self.text) else ''

                while self.isNumber(ch):
                    s += ch
                    i += 1
                    ch = self.text[i] if i < len(self.text) else ''

                if ch in ['\r', '\n', ';', '\t']:
                    self.printResult(s, "科学计数")
                    i += 1
                    return i
                else:
                    self.printError(self.row_number, s, "浮点数错误")
                    return i
            else:
                self.printError(self.row_number, s, "科学计数法错误")
                i += 1
                return i

        #浮点数判断
        elif self.text[i] == '.' and self.isNumber(self.text[i + 1]):
            s += '.'
            i += 1
            ch = self.text[i] if i < len(self.text) else ''

            while self.isNumber(ch):
                s += ch
                i += 1
                ch = self.text[i] if i < len(self.text) else ''

            if ch == 'E':
                if self.text[i + 1] == '+':
                    s += ch
                    i += 1
                    ch = self.text[i]
                    s += ch
                    i += 1
                    ch = self.text[i] if i < len(self.text) else ''
                    while self.isNumber(ch):
                        s += ch
                        i += 1
                        ch = self.text[i] if i < len(self.text) else ''
                    if ch in ['\r', '\n', ';', '\t']:
                        self.printResult(s, "科学计数")
                        i += 1
                        return i
                    else:
                        self.printError(i, s, "浮点数错误")
                        return i
                elif self.isNumber(self.text[i + 1]):
                    s += ch
                    i += 1
                    ch = self.text[i] if i < len(self.text) else ''
                    while self.isNumber(ch):
                        s += ch
                        i += 1
                        ch = self.text[i] if i < len(self.text) else ''
                    if ch in ['\r', '\n', ';', '\t']:
                        self.printResult(s, "科学计数")
                        i += 1
                        return  i
                    else:
                        self.printError(self.row_number, s, "浮点数错误")
                        return i
                        # No need to increment i as it's already at the next position
                else:
                    self.printError(self.row_number, s, "科学计数法错误")
                    i += 1
                    return i
            elif ch in ['\n', '\r', '\t', ' ', '\0', ',', ';'] or ch not in [',', ';']:
                self.printResult(s, "浮点数")
                return i
                # No need to increment i as it's already at the next position
            elif ch in ['+', '-', '*', '/', '\0']:
                self.printResult(s, "浮点数")
                return i
                # No need to increment i as it's already at the next position
            else:
                while ch not in ['\n', '\t', ' ', '\r', '\0', ';', '.', ',']:
                    s += ch
                    i += 1
                    ch = self.text[i] if i < len(self.text) else ''
                self.printError(self.row_number, s, "不合法的字符")
                return i


        elif ch in ['+', '-', '*', '/', '\0']:
            self.printResult(s, "整数")
            return i
            # No need to increment i as it's already at the next position
        else:
            while i < len(self.text) and self.text[i] not in [' ', '\t', '\n', '\r', '\0']:
                s += self.text[i]
                i += 1
            self.printError(self.row_number, s, "错误的标识符")
            return  i

    def handleChar(self, i, s):
        i += 1
        ch = self.text[i] if i < len(self.text) else ''


        while ch != '\'' and i < len(self.text):
            if ch in ['\r', '\n']:
                self.row_number += 1
            elif ch == '\0':  # In Python, '\0' can be used to represent the null character
                self.printError(self.row_number, s, "单字符错误")
                return i
            s += ch
            i += 1
            ch = self.text[i] if i < len(self.text) else ''

        s += ch
        print(s)
        if len(s) == 3 or s in ["'\\t'", "'\\n'", "'\\r'"]:
            self.printResult(s, "单字符")
        else:
            self.printError(self.row_number, s, "字符溢出")

        return i
"""








            




