from Edge import Edge
from Node import Node


class NFA:
    def __init__(self):
        self.nodeList = []
        self.edgeList = []
        self.tags = [
            "[+]", "-", "[*]", "/", "%", "=", "[(]", "[)]", "[{]", "[}]", ";", ",",
            ">", "[^=]", "<", "[|]", "&", "[_a-zA-Z]", "[_0-9a-zA-Z]", "[^_0-9a-zA-Z]",
            "[1-9]", "[0-9]", "[^0-9]", "!"
        ]

        directOP = ["[+]", "-", "[*]", "/", "%", "="]
        SE = ["[(]", "[)]", "[{]", "[}]", ";", ","]

        self.nodeList.append(Node(0, False, False, ""))
        self.edgeList.append(Edge(0, 0, "epsilon"))

        for i in range(1, 6):
            self.nodeList.append(Node(i, True, False, "OP"))
            self.edgeList.append(Edge(0, i, directOP[i - 1]))

        self.nodeList.append(Node(6, False, False, ""))
        self.edgeList.append(Edge(0, 6, "="))

        for i in range(1, 7):
            self.nodeList.append(Node(i + 6, True, False, "SE"))
            self.edgeList.append(Edge(0, i + 6, SE[i - 1]))

        self.nodeList.append(Node(13, False, False, ""))
        self.edgeList.append(Edge(0, 13, ">"))
        self.nodeList.append(Node(14, True, False, "OP"))
        self.edgeList.append(Edge(13, 14, "="))
        self.nodeList.append(Node(15, True, True, "OP"))
        self.edgeList.append(Edge(13, 15, "[^=]"))

        self.nodeList.append(Node(16, False, False, ""))
        self.edgeList.append(Edge(0, 16, "<"))
        self.nodeList.append(Node(17, True, False, "OP"))
        self.edgeList.append(Edge(16, 17, "="))
        self.nodeList.append(Node(18, True, True, "OP"))
        self.edgeList.append(Edge(16, 18, "[^=]"))

        self.nodeList.append(Node(19, False, False, ""))
        self.nodeList.append(Node(20, True, False, "OP"))
        self.edgeList.append(Edge(0, 19, "[|]"))
        self.edgeList.append(Edge(19, 20, "[|]"))

        self.nodeList.append(Node(21, False, False, ""))
        self.nodeList.append(Node(22, True, False, "OP"))
        self.edgeList.append(Edge(0, 21, "&"))
        self.edgeList.append(Edge(21, 22, "&"))

        self.nodeList.append(Node(23, False, False, ""))
        self.nodeList.append(Node(24, True, True, "IDNorKWorOP"))
        self.edgeList.append(Edge(0, 23, "[_a-zA-Z]"))
        self.edgeList.append(Edge(23, 23, "[_0-9a-zA-Z]"))
        self.edgeList.append(Edge(23, 24, "[^_0-9a-zA-Z]"))

        self.nodeList.append(Node(25, False, False, ""))
        self.nodeList.append(Node(26, True, True, "INT"))
        self.edgeList.append(Edge(0, 25, "[0-9]"))
        self.edgeList.append(Edge(25, 25, "[0-9]"))
        self.edgeList.append(Edge(25, 26, "[^0-9]"))

        self.nodeList.append(Node(27, False, False, ""))
        self.edgeList.append(Edge(0, 27, "!"))
        self.nodeList.append(Node(28, True, False, "OP"))
        self.edgeList.append(Edge(27, 28, "="))
        self.nodeList.append(Node(29, True, True, "OP"))
        self.edgeList.append(Edge(27, 29, "[^=]"))

        self.nodeList.append(Node(30, True, False, "OP"))
        self.edgeList.append(Edge(6, 30, "="))
        self.nodeList.append(Node(31, True, True, "OP"))
        self.edgeList.append(Edge(6, 31, "[^=]"))

        # ... initialize nodeList and edgeList as in the Java version ...
        # The initialization logic is identical to the Java version, so I'll skip it for brevity.

    def __str__(self):
        result = ""
        for e in self.edgeList:
            result += f"{e.fromNodeId}({self.nodeList[e.fromNodeId].isLast},{self.nodeList[e.fromNodeId].needRollback},{self.nodeList[e.fromNodeId].type}) ----- {e.tag} -----> {e.toNodeId}({self.nodeList[e.toNodeId].isLast},{self.nodeList[e.toNodeId].needRollback},{self.nodeList[e.toNodeId].type})\n"
        return result
