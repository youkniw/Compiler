import FirstTable
import FollowTable

from Config import Config
from Formula import Formula
from PredictMap import PredictMap


class TextParse:
    formulas = []  # 产生式
    terminals = []  # 终结符
    nonTerminals = []  # 非终结符
    firsts = {}
    follows = {}
    predictions = {}

    @staticmethod
    def writeAllIntoFile():
        try:
            with open(Config.formulaPath, 'w') as out:
                for formula in TextParse.formulas:
                    # Python中数组转字符串使用 ' '.join() 方法
                    right_side = ', '.join(formula.right)
                    out.write("文法左侧: " + formula.left + "\t" + "文法右侧: [" + right_side + "]\n")
        except Exception as e:
            raise RuntimeError(e)

        try:
            with open(Config.terminalPath, 'w') as out:
                for s in TextParse.terminals:
                    out.write(s + "\n")
        except Exception as e:
            raise RuntimeError(e)

        try:
            with open(Config.nonTerminalPath, 'w') as out:
                for s in TextParse.nonTerminals:
                    out.write(s + "\n")
        except Exception as e:
            raise RuntimeError(e)

        try:
            with open(Config.firstTablePath, 'w') as out:
                for s in TextParse.firsts.keys():
                    # 将列表转换为字符串
                    values = ', '.join(TextParse.firsts[s])
                    out.write(s + "\t" + values + "\n")
        except Exception as e:
            raise RuntimeError(e)

        try:
            with open(Config.followTablePath, 'w') as out:
                for s in TextParse.follows.keys():
                    values = ', '.join(TextParse.follows[s])
                    out.write(s + "\t" + values + "\n")
        except Exception as e:
            raise RuntimeError(e)

        try:
            with open(Config.predictMapPath, 'w') as out:
                for s in TextParse.predictions.keys():
                    formula = TextParse.predictions[s]
                    right_side = ' '.join(formula.right)
                    out.write(s + "\t" + "文法: " + formula.left + "->" + right_side + "\n")
        except Exception as e:
            raise RuntimeError(e)

    @staticmethod
    def Do():
        # 初始化各种数据结构
        TextParse.formulas = []
        TextParse.terminals = []
        TextParse.non_terminals = []
        TextParse.firsts = {}
        TextParse.follows = {}
        TextParse.predictions = {}
        # 设置 formulas, non_terminals 等，需要具体的逻辑
        TextParse.setFormulas()
        TextParse.setNonTerminals()
        TextParse.setTerminals()
        TextParse.setFirsts()
        TextParse.setFollows()
        TextParse.setPrediction()

    @staticmethod
    def setFormulas():
        try:
            with open(Config.grammarPath, 'r') as file:
                for line in file:
                    left, right = line.strip().split("->")
                    formula = Formula(left.strip(), right.strip().split(" "))
                    TextParse.formulas.append(formula)
        except Exception as e:
            print(e)

    @staticmethod
    def setNonTerminals():
        # 解析文法中的非终结符
        for formula in TextParse.formulas:
            if formula.left not in TextParse.nonTerminals:
                TextParse.nonTerminals.append(formula.left)

    @staticmethod
    def setTerminals():
        for formula in TextParse.formulas:
            rights = formula.returnRights()  # 在 Python 中，right 已经是一个列表
            for s in rights:
                if s not in TextParse.nonTerminals and s != "$":
                        TextParse.terminals.append(s)

    @staticmethod
    def setFirsts():
        FirstTable.FirstTable.setFirst(TextParse.formulas, TextParse.terminals, TextParse.nonTerminals,
                                       TextParse.firsts)

    @staticmethod
    def setFollows():
        FollowTable.FollowTable.setFollow(TextParse.formulas, TextParse.terminals, TextParse.nonTerminals,
                                          TextParse.firsts, TextParse.follows)

    @staticmethod
    def setPrediction():
        PredictMap.setPrediction(TextParse.formulas, TextParse.terminals, TextParse.nonTerminals, TextParse.firsts,
                                 TextParse.follows, TextParse.predictions)
