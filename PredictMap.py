from Formula import Formula


class PredictMap:
    @staticmethod
    def setPrediction(formulas, terminals, non_terminals, firsts, follows, predictions):
        # 第一部分
        for formula in formulas:
            if formula.right[0] == "$":
                continue
            try:
                for terminal_in_firsts in firsts.get(formula.right[0]):
                    if terminal_in_firsts == "$":
                        for terminal_in_follows in follows.get(formula.left):
                            key = PredictMap.get_map_key(terminal_in_follows, formula.left)
                            predictions[key] = Formula(formula.left, ["$"])
                    else:
                        key = PredictMap.get_map_key(terminal_in_firsts, formula.left)
                        predictions[key] = formula
            except Exception as e:
                print("First 集合中没有 key:", formula.right[0])
                print(e)

        # 第二部分
        for formula in formulas:
            if formula.right[0] == "$":
                for follow_element in follows.get(formula.left):
                    key = PredictMap.get_map_key(follow_element, formula.left)
                    predictions[key] = formula

    @staticmethod
    def get_map_key(terminal, non_terminal):
        return f"{{横坐标: {terminal}  纵坐标: {non_terminal}}}"
