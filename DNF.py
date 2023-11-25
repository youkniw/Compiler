import re
from collections import deque

from Edge import Edge
from Node import Node


class DFA:
    TYPE_TO_CONTENT_DICT_KW = {
        "int": 1,
        "void": 2,
        "return": 3,
        "const": 4,
        "main": 5,
        "struct": 6
    }

    TYPE_TO_CONTENT_DICT_OP = {
        "+": 7,
        "-": 8,
        "*": 9,
        "/": 10,
        "%": 11,
        "=": 12,
        ">": 13,
        "<": 14,
        "==": 15,
        "<=": 16,
        ">=": 17,
        "!=": 18,
        "&&": 19,
        "||": 20,
        "!": 21
    }

    TYPE_TO_CONTENT_DICT_SE = {
        "(": 22,
        ")": 23,
        "{": 24,
        "}": 25,
        ";": 26,
        ",": 27
    }

    def __init__(self, nfa):
        self.nfa = nfa
        self.nodeList = []
        self.edgeList = []
        self.nowId = None
        self.startId = None

    # ... Other methods ...

    def epsilonClosure(self, node_set):
        q = deque(node_set)
        while q:
            top = q.popleft()
            for e in self.nfa.edgeList:
                if e.tag == "epsilon" and top.id == e.fromNodeId:
                    if self.nfa.nodeList[e.toNodeId] in node_set:
                        continue
                    node_set.add(self.nfa.nodeList[e.toNodeId])
                    q.append(self.nfa.nodeList[e.toNodeId])
        return node_set

    def move(self, node_set, a):
        res = set()
        for n in node_set:
            for e in self.nfa.edgeList:
                if e.tag == a and n.id == e.fromNodeId:
                    res.add(self.nfa.nodeList[e.toNodeId])
        return res

    # ... Other methods ...
    def convertNFAToDFA(self):
        self.nodeList.append(Node(0, False, False, ""))
        initial_node_set = self.epsilonClosure({self.nfa.nodeList[0]})
        node_sets = [initial_node_set]

        pointer = 0
        while pointer < len(node_sets):
            current_node_set = node_sets[pointer]
            for tag in self.nfa.tags:
                next_node_set = self.epsilonClosure(self.move(current_node_set, tag))
                if not next_node_set:
                    continue

                self.processNodeSet(node_sets, current_node_set, next_node_set, tag, pointer)
            pointer += 1

    def processNodeSet(self, node_sets, current_node_set, next_node_set, tag, current_id):
        if next_node_set not in node_sets:
            node_sets.append(next_node_set)
            first_in_set = min(next_node_set, key=lambda node: node.id)
            new_id = len(self.nodeList)
            self.nodeList.append(Node(new_id, first_in_set.isLast, first_in_set.needRollback, first_in_set.type))
            self.edgeList.append(Edge(current_id, new_id, tag))
        else:
            existing_id = node_sets.index(next_node_set)
            self.edgeList.append(Edge(current_id, existing_id, tag))

    def minimizeDFA(self):
        # Initializing sets
        P = []
        F = set()
        NF = set()

        # Partitioning nodes into final (F) and non-final (NF) states
        for n in self.nodeList:
            if n.isLast:
                F.add(n)
            else:
                NF.add(n)

        P.append(F)
        P.append(NF)

        W = [F, NF]

        while W:
            A = W.pop(0)
            remove_of_p = None  # Reset remove_of_p at the start of each iteration

            for tag in self.nfa.tags:
                X = []
                for p in P:
                    p_tag = {n for n in p if
                             any((e.fromNodeId == n.id or e.toNodeId == n.id) and e.tag == tag for e in self.edgeList)}
                    p_not_tag = p - p_tag

                    if p_tag and p_not_tag:
                        X.extend([p_tag, p_not_tag])
                        remove_of_p = p
                        break

                if remove_of_p and remove_of_p in P:  # Check if remove_of_p exists in P before removing
                    P.remove(remove_of_p)
                    P.extend(X)

                    for x in X:
                        if x not in W:
                            W.append(x)
                        else:
                            W.remove(x)

        # Creating new node and edge lists
        new_node_list = []
        new_edge_list = []

        for i, p in enumerate(P):
            first_in_set = min(p, key=lambda node: node.id)
            new_node_list.append(Node(i, first_in_set.isLast, first_in_set.needRollback, first_in_set.type))

        for e in self.edgeList:
            from_node_id = next(i for i, p in enumerate(P) if self.nodeList[e.fromNodeId] in p)
            to_node_id = next(i for i, p in enumerate(P) if self.nodeList[e.toNodeId] in p)
            new_edge_list.append(Edge(from_node_id, to_node_id, e.tag))

        self.edgeList = new_edge_list
        self.nodeList = new_node_list
        self.startId = 1
        self.nowId = 1








    def __str__(self):
        result = "DFA节点数: {}\n".format(len(self.nodeList))
        for e in self.edgeList:
            from_node = self.nodeList[e.fromNodeId]
            to_node = self.nodeList[e.toNodeId]
            result += "{}({},{},{}) ----- {} -----> {}({},{},{})\n".format(
                e.fromNodeId, from_node.isLast, from_node.needRollback, from_node.type,
                e.tag, e.toNodeId, to_node.isLast, to_node.needRollback, to_node.type
            )
        return result

    def nextId(self, tag):
        for edge in self.edgeList:
            if edge.fromNodeId == self.nowId and re.match(edge.tag, tag):
                self.nowId = edge.toNodeId
                return True
        print(tag)
        return False

    # ... Other methods ...



    def isFinal(self, id):
            return self.nodeList[id].isLast

    def isBackOff(self, id):
            return self.nodeList[id].needRollback

    def getType(self, id):
            return self.nodeList[id].type

    def getTokenType(self, token, node_tag):
            if node_tag in ["OP", "SE", "INT"]:
                return node_tag
            elif node_tag == "IDNorKWorOP":
                keywords = DFA.TYPE_TO_CONTENT_DICT_KW.keys()
                ops = DFA.TYPE_TO_CONTENT_DICT_OP.keys()
                if token in keywords:
                    return "KW"
                elif token in ops:
                    return "OP"
                else:
                    return "IDN"
            else:
                return "ERROR"

    def getTokenTypeSelf(self, token, node_tag):
        if node_tag in ["OP", "SE"]:
            return token
        elif node_tag == "INT":
            return node_tag
        elif node_tag == "IDNorKWorOP":
            keywords = DFA.TYPE_TO_CONTENT_DICT_KW.keys()
            ops = DFA.TYPE_TO_CONTENT_DICT_OP.keys()
            if token in keywords:
                return token
            elif token in ops:
                return "OP"
            else:
                return "Ident"
        else:
            return "ERROR"

    def getTokenNum(self, token, token_type):
        if token_type in ["IDN", "INT"]:
            return token
        elif token_type == "KW":
            return str(DFA.TYPE_TO_CONTENT_DICT_KW.get(token))
        elif token_type == "OP":
            return str(DFA.TYPE_TO_CONTENT_DICT_OP.get(token))
        elif token_type == "SE":
            return str(DFA.TYPE_TO_CONTENT_DICT_SE.get(token))
        else:
            return "error"

    def getStart(self):
        self.nowId = self.startId
