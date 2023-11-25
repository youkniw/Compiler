from Config import Config
from do import do
from PredictMap import PredictMap
from TextParse import TextParse


class MainParse:
    predict_map = {}  # 预测表
    input_str = []  # 输入串, 词法分析的结果
    symbol_stack = []  # 符号栈
    parse_result_stack = []  # 语法分析输出展示的结果
    parse_result_counter = 0  # 语法分析输出结果的计数器

    @staticmethod
    def DoParse(file):
        do(file)
        # 词法分析的输入
        file_path = "D:\python\pythonProject\output\\file"
        MainParse.parse_lexical_output_from_file(file_path)
        MainParse.symbol_stack = []
        MainParse.parse_result_stack = []
        MainParse.parse_result_counter = 0

        TextParse.Do()  # 生成各种表，First，Follow，预测表
        MainParse.predict_map = TextParse.predictions  # 预测表

        TextParse.writeAllIntoFile()  # 将语法分析开始前生成的所有表打印出来
        MainParse.writeLexiconMiddleResultIntoFile()  # 将词法分析的中间结果打印出来

        MainParse.parse()  # 开始语法分析

        MainParse.printParseResult()  # 打印语法分析结果

    @staticmethod
    def writeLexiconMiddleResultIntoFile():
        try:
            with open(Config.lexiconMiddleResult, 'w') as out:
                for s in MainParse.input_str:
                    # 假设 s 是一个元组，例如 ('IDN', 'a')
                    token_type, token_value = s
                    out.write(f"{token_type} <{token_value}>\n")  # 格式化字符串
        except IOError as e:
            print(f"写入文件错误: {e}")

    @staticmethod
    def parse_lexical_output_from_file(file_path):
        with open(file_path, 'r') as lexical_output:
            for line in lexical_output:
                parts = line.strip().split()
                if len(parts) >= 2:

                    token_info = parts[1].strip('<>').split(',')
                    if len(token_info) >= 2:

                        token_type = token_info[0]
                        if token_type == "":
                            token_type = ","
                        token_value = parts[0]
                        MainParse.input_str.append((token_type, token_value))

    @staticmethod
    def parse():
        MainParse.symbol_stack.append("#")
        MainParse.input_str.append(("#", "#"))  # 添加类型和值的元组

        MainParse.symbol_stack.append(Config.initSymbol)

        while True:
            MainParse.parse_result_counter += 1
            current_token_type, current_token_value = MainParse.input_str[0]

            if MainParse.symbol_stack[-1] == "#" and current_token_type == "#":
                MainParse.parse_result_stack.append(
                    f"{MainParse.parse_result_counter}\tEOF#EOF\taccept")
                break

            try:
                if current_token_type == MainParse.symbol_stack[-1]:
                    MainParse.parse_result_stack.append(
                        f"{MainParse.parse_result_counter}\t"
                        f"{MainParse.symbol_stack[-1]}#{current_token_value}\tmove")
                    MainParse.input_str.pop(0)
                    MainParse.symbol_stack.pop()
                    continue
            except Exception as e:
                print(e)

            predict_map_key = PredictMap.get_map_key(
                current_token_type, MainParse.symbol_stack[-1])

            formula = MainParse.predict_map.get(predict_map_key)
            if formula is not None:
                MainParse.parse_result_stack.append(
                    f"{MainParse.parse_result_counter}\t"
                    f"{MainParse.symbol_stack[-1]}#{current_token_value}\treduction")
                if MainParse.symbol_stack[-1] != "#":
                    MainParse.symbol_stack.pop()
                rights = formula.returnRights()
                if rights[0] != "$":
                    for i in range(len(rights) - 1, -1, -1):
                        MainParse.symbol_stack.append(rights[i])
            else:
                MainParse.parse_result_stack.append(
                    f"{MainParse.parse_result_counter}\t"
                    f"{MainParse.symbol_stack[-1]}#{current_token_value}\terror")
                return

    """
    @staticmethod
    def parse():

        MainParse.symbol_stack.append("#")
        MainParse.input_str.append("#")

        MainParse.symbol_stack.append(Config.initSymbol)

        while True:
            MainParse.parse_result_counter += 1
            if MainParse.symbol_stack[-1] == "#" and MainParse.input_str[0] == "#":
                MainParse.parse_result_stack.append(
                    f"{MainParse.parse_result_counter}\tEOF#EOF\taccept")
                break

            try:
                if MainParse.input_str[0] == MainParse.symbol_stack[-1]:
                    MainParse.parse_result_stack.append(
                        f"{MainParse.parse_result_counter}\t"
                        f"{MainParse.symbol_stack[-1]}#{MainParse.input_str[0]}\tmove")
                    MainParse.input_str.pop(0)
                    MainParse.symbol_stack.pop()
                    continue
            except Exception as e:
                print(e)

            predict_map_key = PredictMap.get_map_key(
                MainParse.input_str[0], MainParse.symbol_stack[-1])

            formula = MainParse.predict_map.get(predict_map_key)
            if formula is not None:
                MainParse.parse_result_stack.append(
                    f"{MainParse.parse_result_counter}\t"
                    f"{MainParse.symbol_stack[-1]}#{MainParse.input_str[0]}\treduction")
                if MainParse.symbol_stack[-1] != "#":
                    MainParse.symbol_stack.pop()
                rights = formula.returnRights()
                if rights[0] != "$":
                    for i in range(len(rights) - 1, -1, -1):
                        MainParse.symbol_stack.append(rights[i])
            else:
                MainParse.parse_result_stack.append(
                    f"{MainParse.parse_result_counter}\t"
                    f"{MainParse.symbol_stack[-1]}#{MainParse.input_str[0]}\terror")
                return
    """
    """
    @staticmethod
    def parse():
        MainParse.symbol_stack.append("#")
        MainParse.input_str.append(("#", "#"))  # 添加类型和值的元组

        MainParse.symbol_stack.append(Config.initSymbol)

        while True:
            MainParse.parse_result_counter += 1
            current_token_type, current_token_value = MainParse.input_str[0]

            if MainParse.symbol_stack[-1] == "#" and current_token_type == "#":
                MainParse.parse_result_stack.append(
                    f"{MainParse.parse_result_counter}\tEOF#EOF\taccept")
                break

            try:
                if current_token_type == MainParse.symbol_stack[-1]:
                    MainParse.parse_result_stack.append(
                        f"{MainParse.parse_result_counter}\t"
                        f"{MainParse.symbol_stack[-1]}#{current_token_value}\tmove")
                    MainParse.input_str.pop(0)
                    MainParse.symbol_stack.pop()
                    continue
            except Exception as e:
                print(e)

            predict_map_key = PredictMap.get_map_key(
                current_token_type, MainParse.symbol_stack[-1])

            formula = MainParse.predict_map.get(predict_map_key)
            if formula is not None:
                MainParse.parse_result_stack.append(
                    f"{MainParse.parse_result_counter}\t"
                    f"{MainParse.symbol_stack[-1]}#{current_token_value}\treduction")
                if MainParse.symbol_stack[-1] != "#":
                    MainParse.symbol_stack.pop()
                rights = formula.returnRights()
                if rights[0] != "$":
                    for i in range(len(rights) - 1, -1, -1):
                        MainParse.symbol_stack.append(rights[i])
            else:
                MainParse.parse_result_stack.append(
                    f"{MainParse.parse_result_counter}\t"
                    f"{MainParse.symbol_stack[-1]}#{current_token_value}\terror")
                return
    """

    @staticmethod
    def printParseResult():
        # ...（打印语法分析结果的具体实现）
        print("开始输出语法分析结果: --------------------")
        for s in MainParse.parse_result_stack:
            print(s)

        try:
            with open(Config.parseResultPath, 'w') as out:
                for s in MainParse.parse_result_stack:
                    out.write(s + "\n")
        except Exception as e:
            print(e)
