class FirstTable:
    formulas = []
    terminals = []
    nonTerminals = []
    firsts = {}

    @staticmethod
    def setFirst(_formulas, _terminals, _nonTerminals, _firsts):
        FirstTable.formulas = _formulas
        FirstTable.terminals = _terminals
        FirstTable.nonTerminals = _nonTerminals
        FirstTable.firsts = _firsts

        # 初始化终结符的 First 集合
        for terminal in FirstTable.terminals:
            FirstTable.firsts[terminal] = [terminal]

        # 为所有非终结符注册空 First 集合
        for nonTerminals in FirstTable.nonTerminals:
            FirstTable.firsts[nonTerminals] = []

        # 计算 First 集合
        while True:
            flag = True
            for formula in FirstTable.formulas:
                left = formula.returnLeft()
                rights = formula.returnRights()

                for right in rights:
                    if right != "$":
                        for item in FirstTable.firsts[right]:
                            if item not in FirstTable.firsts[left]:
                                FirstTable.firsts[left].append(item)
                                flag = False

                    if not FirstTable.isCanBeNull(FirstTable.formulas,right):
                        break

            if flag:
                break

    @staticmethod
    def recursion(cur):
        if cur in FirstTable.terminals:
            return FirstTable.firsts[cur]

        if len(FirstTable.firsts[cur]) != 0:
            return FirstTable.firsts[cur]

        for formula in FirstTable.formulas:
            if formula.returnLeft() == cur:
                first_right = formula.returnRights()[0]
                tmp = FirstTable.recursion(first_right)
                for s in tmp:
                    if s not in FirstTable.firsts[cur]:
                        FirstTable.firsts[cur].append(s)
        return FirstTable.firsts[cur]

    @staticmethod
    def isCanBeNull(formulas,symbol):
        for formula in formulas:
            if formula.returnLeft() == symbol:
                rights = formula.returnRights()
                if rights[0] == "$":
                    return True
        return False


