from Config import Config


class FollowTable:
    @staticmethod
    def setFollow(formulas, terminals, non_terminals, firsts, follows):
        # 初始化所有非终结符的 Follow 集合
        for non_terminal in non_terminals:
            follows[non_terminal] = []

        # 将 '#' 添加到起始符号的 Follow 集合中
        follows[Config.initSymbol].append("#")

        while True:
            flag = True

            for formula in formulas:
                rights = formula.returnRights()

                for j in range(len(rights)):
                    right = rights[j]

                    if right in non_terminals:
                        fab = True
                        for k in range(j + 1, len(rights)):
                            for v in firsts[rights[k]]:
                                if v not in follows[right]:
                                    follows[right].append(v)
                                    flag = False

                            if not FollowTable.is_can_be_null(formulas,rights[k]):
                                fab = False
                                break

                        if fab:
                            left = formula.returnLeft()
                            for p in follows[left]:
                                if p not in follows[right]:
                                    follows[right].append(p)
                                    flag = False

            if flag:
                break

        # 清除 Follow 集合中的 '#'
        for non_terminal in non_terminals:
            follows[non_terminal] = [x for x in follows[non_terminal] if x != "#"]

        # 为所有非终结符的 Follow 集合加上 '#'
        for non_terminal in non_terminals:
            if "#" not in follows[non_terminal]:
                follows[non_terminal].append("#")

    @staticmethod
    def is_can_be_null(formulas, symbol):
        for formula in formulas:
            if formula.returnLeft() == symbol and formula.returnRights()[0] == "$":
                return True
        return False
