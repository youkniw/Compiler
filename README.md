 Compiler


# 天津大学编译原理大作业

* 完成词法分析
* 完成语法分析

## 代码结构

```bash
compiler
    |- input
        |- grammer.txt
        |- 测试文件
        |- ...
    |- output
        |- file.txt
        |- First集合.txt
        |- Follow集合.txt
        |- 分析表.txt
        |- 文法.txt
        |- 终结符.txt
        |- 词法分析产生的中间结果.txt
        |- 非终结符.txt
    |- result
        |- gra.tsv
        |- lex.tsv
    |- src
        |- Config.py
        |- TextLexicon.py
        |- TextLexiconInput.py
        |- MainLexicon.py
        |- FirstTable.py
        |- FollowTable.py
        |- PredictMap.py
        |- TextParse.py
        |- TextParseInput.py
        |- MainParse.py
        |- Main.py
    |- README.md
```

Config: 一些配置

TextLexicon: 词法分析的主类

MainLexicon: 词法分析的入口类

TextLexiconInput: 词法分析的输入类

TextParseInput: 语法分析的输入类

TextParse: 语法分析中负责解析文法，生成First表，Follow表，预测表的类

MainParse: 利用语法分析的输入和预测表进行语法分析的类

FirstTable: 生成First表的类

FollowTable: 生成Follow表的类

PredictMap: 生成预测表的类

Formula: 表示文法的类

## 源程序编译步骤

Main.java 为入口文件，从 Main.java 进行编译。

## 一、词法分析器设计

### 1. 实现路径

#### 1.1 实现思路

读取c--文件，存放为字符串类型。遍历整个字符串，将结果存放于三元组数组中，将中间结果也存放于数组中，输出后作为语法分析的输入

#### 1.2 需要实现的单词符号

1. 关键字（KW，不区分大小写）包括： (1) int (2) void (3) return (4) const (5) main
2. 运算符（OP）包括：(6) + (7) - (8) * (9) / (10) % (11) = (12) > (13) < (14) == (15) <= (16) >= (17) != (18) && (19) ||
3. 界符（SE）包括：(20)（ (21) ） (22) { (23) } (24)； (25) ,
4. 标识符（IDN）定义与 C 语言保持相同，为字母、数字和下划线（_）组成的不以数字开头的串
5. 整数（INT）的定义与 C 语言类似，整数由数字串表示

### 2. 算法描述

运用面向对象的编程思想，创建TextLexicon类和MainLexicon类。
由简到繁，先将类的定义规划好，再逐渐扩充完善细节。

#### 2.1 TextLexicon类定义与实现

设置threeElements，lex\_result\_stack，lex\_error\_stack，text\_length，row\_numberKey 六个属性，分别代表要输出的三元组，得出的文本的值，可能出现的错误，输入文本的长度，输入文本行号，关键字。使用面向对象的编程方式来进行词法分析器的编写。

**类中的方法：**

- isAlpha方法

用于判断当前字符是否为字母或下划线。

```java
public int isAlpha(char c){
    if(((c<='z')&&(c>='a')) || ((c<='Z')&&(c>='A')) || (c=='_'))
        return 1;
    else
        return 0;
}
```

- isNumber方法

用于判断当前字符是否为数字。。

```java
public int isNumber(char c) {
    if ((c >= '0') && (c <= '9'))
        return 1;
    else
        return 0;
}
```

- isKey方法

用于判断当前字符串是否为关键字。

```java
public int isKey(String t) {
    for (int i = 0; i < Key.length; i++) {
        if (t.equals(Key[i])) {
            return 1;
        }
    }
    return 0;
}
```

- scannerAll方法

用于遍历读取的整个c--文本字符串。

```java
public void scannerAll() {
    int i = 0;
    char c;
    text = text + '\0';
    while (i < text_length) {
        c = text.charAt(i);
        if (c == ' ' || c == '\t')
            i++;
        else if (c == '\r' || c == '\n') {
            row_number++;
            i++;
        } else
            i = scannerPart(i);
    }
}
```

- scannerPart方法

用于扫描字符串单元。

```java
public int scannerPart(int arg0) {
    int i = arg0;
    char ch = text.charAt(i);
    String s = "";
    // 第一个输入的字符是字母
    if (isAlpha(ch) == 1) {
        s = "" + ch;
        return handleFirstAlpha(i, s);
    }
    // 第一个是数字的话
    else if (isNumber(ch) == 1) {
        s = "" + ch;
        return handleFirstNum(i, s);

    }
    // 既不是既不是数字也不是字母
    else {
        s = "" + ch;
        switch (ch) {
        case ' ':
        case '\n':
        case '\r':
        case '\t':
            return ++i;
        case '[':
        case ']':
        case '(':
        case ')':
        case '{':
        case '}':
            printResult(s, "双界符");
            return ++i;
        case ':':
            if (text.charAt(i + 1) == '=') {
                s = s + "=";
                printResult(s, "界符");
                return i + 2;
            } else {
                printError(row_number, s, "不能识别");
                return i + 1;
            }
        case ',':
        case '.':
        case ';':
            printResult(s, "单界符");
            return ++i;
        case '\\':
            if (text.charAt(i + 1) == 'n' || text.charAt(i + 1) == 't' || text.charAt(i + 1) == 'r') {
                printResult(s + text.charAt(i + 1), "转义");
                return i + 2;
            }
        case '\'':
            // 判断是否为单字符，否则报错
            return handleChar(i, s);
        case '\"':
            // 判定字符串
            return handleString(i, s);
        case '+':
            return handlePlus(i, s);
        case '-':
            return handleMinus(i, s);
        case '*':
        case '/':
            if (text.charAt(i + 1) == '*') {
                return handleNote(i, s);
            } else if (text.charAt(i + 1) == '/') {
                return handleSingleLineNote(i, s);
            }
        case '!':
        case '=':
            ch = text.charAt(++i);
            if (ch == '=') {
                // 输出运算符
                s = s + ch;
                printResult(s, "运算符");
                return ++i;
            } else {
                // 输出运算符
                printResult(s, "运算符");
                return i;
            }
        case '>':
            return handleMore(i, s);
        case '<':
            return handleLess(i, s);
        case '%':
            ch = text.charAt(++i);
            if (ch == '=') {
                // 输出运算符
                s = s + ch;
                printResult(s, "运算符");
                return ++i;
            } else if (ch == 's' || ch == 'c' || ch == 'd' || ch == 'f' || ch == 'l') {
                // 输出类型标识符
                s = s + ch;
                printResult(s, "输出类型标识符");
                return ++i;
            } else {
                // 输出求余标识符
                printResult(s, "求余标识符");
                return i;
            }
        default:
            // 输出暂时无法识别的字符,制表符也被当成了有问题的字符
            printError(row_number, s, "暂时无法识别的标识符");
            return ++i;
        }
    }
}
```

- handleFirstAlpha方法

用于处理字符串单元的第一个输入为字母或下划线的情况

```java
public int handleFirstAlpha(int arg, String arg0) {
    int i = arg;
    String s = arg0;
    char ch = text.charAt(++i);
    while (isAlpha(ch) == 1 || isNumber(ch) == 1) {
        s = s + ch;
        ch = text.charAt(++i);
    }
    // if(s.length()==1){
    // printResult(s, "字符常数");
    // return i;
    // }
    // 到了结尾
    if (isKey(s) == 1) {
        // 输出key
        printResult(s, "关键字");
        return i;

    } else {
        // 输出普通的标识符
        printResult(s, "标识符");
        return i;
    }
}
```

- handleFirstNum方法

用于处理字符串单元的第一个输入为数字的情况

```java
public int handleFirstNum(int arg, String arg0) {
    int i = arg;
    char ch = text.charAt(++i);
    String s = arg0;
    while (isNumber(ch) == 1) {
        s = s + ch;
        ch = text.charAt(++i);
    }
    if ((text.charAt(i) == ' ') || (text.charAt(i) == '\t') || (text.charAt(i) == '\n') || (text.charAt(i) == '\r')
            || (text.charAt(i) == '\0') || ch == ';' || ch == ',' || ch == ')' || ch == ']' || ch == '['
            || ch == '(') {
        // 到了结尾，输出数字
        printResult(s, "整数");
        return i;
    } else if (ch == 'E') {
        if (text.charAt(i + 1) == '+') {
            s = s + ch;
            ch = text.charAt(++i);
            s = s + ch;
            ch = text.charAt(++i);
            while (isNumber(ch) == 1) {
                s = s + ch;
                ch = text.charAt(++i);
            }
            if (ch == '\r' || ch == '\n' || ch == ';' || ch == '\t') {
                printResult(s, "科学计数");
                return ++i;
            } else {
                printError(i, s, "浮点数错误");
                return i;
            }
        } else if (isNumber(text.charAt(i + 1)) == 1) {
            s = s + ch;
            ch = text.charAt(++i);
            while (isNumber(ch) == 1) {
                s = s + ch;
                ch = text.charAt(++i);
            }
            if (ch == '\r' || ch == '\n' || ch == ';' || ch == '\t') {
                printResult(s, "科学计数");
                return ++i;
            } else {
                printError(row_number, s, "浮点数错误");
                return i;
            }
        } else {
            printError(row_number, s, "科学计数法错误");
            return ++i;
        }
    }

    // 浮点数判断
    else if (text.charAt(i) == '.' && (isNumber(text.charAt(i + 1)) == 1)) {
        s = s + '.';
        ch = text.charAt(++i);
        while (isNumber(ch) == 1) {
            s = s + ch;
            ch = text.charAt(++i);
        }
        if (ch == 'E') {
            if (text.charAt(i + 1) == '+') {
                s = s + ch;
                ch = text.charAt(++i);
                s = s + ch;
                ch = text.charAt(++i);
                while (isNumber(ch) == 1) {
                    s = s + ch;
                    ch = text.charAt(++i);
                }
                if (ch == '\r' || ch == '\n' || ch == ';' || ch == '\t') {
                    printResult(s, "科学计数");
                    return ++i;
                } else {
                    printError(i, s, "浮点数错误");
                    return i;
                }
            } else if (isNumber(text.charAt(i + 1)) == 1) {
                s = s + ch;
                ch = text.charAt(++i);
                while (isNumber(ch) == 1) {
                    s = s + ch;
                    ch = text.charAt(++i);
                }
                if (ch == '\r' || ch == '\n' || ch == ';' || ch == '\t') {
                    printResult(s, "科学计数");
                    return ++i;
                } else {
                    printError(row_number, s, "浮点数错误");
                    return i;
                }
            } else {
                printError(row_number, s, "科学计数法错误");
                return ++i;
            }
        } else if (ch == '\n' || ch == '\r' || ch == '\t' || ch == ' ' || ch == '\0' || ch != ',' || ch != ';') {
            printResult(s, "浮点数");
            return i;
        } else if (ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '\0') {
            printResult(s, "浮点数");
            return i;
        } else {
            while (ch != '\n' && ch != '\t' && ch != ' ' && ch != '\r' && ch != '\0' && ch != ';' && ch != '.'
                    && ch != ',') {
                s = s + ch;
                ch = text.charAt(++i);
            }
            printError(row_number, s, "不合法的字符");
            return i;
        }
    } else if (ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '\0') {
        printResult(s, "整数");
        return i;
    } else {
        do {
            ch = text.charAt(i++);
            s = s + ch;
        } while ((text.charAt(i) != ' ') && (text.charAt(i) != '\t') && (text.charAt(i) != '\n')
                && (text.charAt(i) != '\r') && (text.charAt(i) != '\0'));
        printError(row_number, s, "错误的标识符");
        return i;
    }
}
```

- printResult方法

用于将中间结果和最终结果添加到lex_result_stack数组和threeElements数组中。

```java
public void printResult(String rs_value, String rs_name) {
    if (rs_name.equals("标识符")) {
        lex_result_stack.add("Ident");
        threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "IDN", rs_value)));
    } else if (rs_name.equals("整数")) {
        lex_result_stack.add("INT");
        threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "INT", rs_value)));
    } else if (rs_name.equals("科学计数") || rs_name.equals("浮点数")) {
        lex_result_stack.add("float");
        threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "FLOAT", rs_value)));
    } else if (rs_name.equals("单字符")) {
        lex_result_stack.add("char");
        threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "CHAR", rs_value)));
    } else if (rs_name.equals("字符串")) {
        lex_result_stack.add("str");
        threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "STR", rs_value)));
    } else if (rs_name.equals("运算符")) {
        lex_result_stack.add(rs_value);
        if (rs_value.equals("+")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "6")));
        } else if (rs_value.equals("-")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "7")));
        } else if (rs_value.equals("*")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "8")));
        } else if (rs_value.equals("/")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "9")));
        } else if (rs_value.equals("%")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "10")));
        } else if (rs_value.equals("=")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "11")));
        } else if (rs_value.equals(">")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "12")));
        } else if (rs_value.equals("<")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "13")));
        } else if (rs_value.equals("==")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "14")));
        } else if (rs_value.equals("<=")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "15")));
        } else if (rs_value.equals(">=")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "16")));
        } else if (rs_value.equals("!=")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "17")));
        } else if (rs_value.equals("&&")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "18")));
        } else if (rs_value.equals("||")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "OP", "19")));
        }
    } else if (rs_name.equals("单界符") || rs_name.equals("双界符")) {
        lex_result_stack.add(rs_value);
        if (rs_value.equals("(")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "SE", "20")));
        } else if (rs_value.equals(")")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "SE", "21")));
        } else if (rs_value.equals("{")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "SE", "22")));
        } else if (rs_value.equals("}")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "SE", "23")));
        } else if (rs_value.equals(";")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "SE", "24")));
        } else if (rs_value.equals(",")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "SE", "25")));
        }
    } else if (rs_name.equals("关键字")) {
        lex_result_stack.add(rs_value);
        if (rs_value.equals("int")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "KW", "1")));
        } else if (rs_value.equals("void")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "KW", "2")));
        } else if (rs_value.equals("return")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "KW", "3")));
        } else if (rs_value.equals("const")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "KW", "4")));
        } else if (rs_value.equals("main")) {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "KW", "5")));
        } else {
            threeElements.add(new ArrayList<>(Arrays.asList(rs_value, "KW", rs_value)));
        }
    }
}
```

- printError方法

用于打印错误信息。

```java
public void printError(int row_num, String rs_value, String rs_name) {
    HashMap<String, String> hashMap = new HashMap<String, String>();
    hashMap.put("行号：", row_num + "");
    hashMap.put("输入：", rs_value);
    hashMap.put("错误类型: ", rs_name);
    lex_error_stack.add(hashMap);
    // tbModel_lex_result.addRow(new String[]{"ERROR，"+rs_name, rs_value});
}
```

#### 2.2MainLexicon类的定义与实现

此类主要定义了词法分析的入口函数，用于打印词法分析结果及将结果输出到文件中。

```java
public static void DoLex() {
    String content = TextLexiconInput.input(); // 得到文本内容
    TextLexicon textLexicon = new TextLexicon(content); // 将文本内容给词法编译器
    textLexicon.scannerAll();   // 入口函数
    ArrayList<HashMap<String, String>> lex_error_stack = textLexicon.get_Lex_Error();
    if (lex_error_stack.size() != 0) {  // 错误信息不为空
        System.out.println("词法分析阶段出现错误！");
        for (HashMap<String, String> stringStringHashMap : lex_error_stack) {   // 输出错误信息
            System.out.println(stringStringHashMap);
        }
        return; // 词法分析中断
    }
    ArrayList<ArrayList<String>> threeElements = textLexicon.getThreeElements(); // 得到要输出的三元组
    // 打印
    System.out.println("开始输出词法分析结果: ---------------------");
    for (ArrayList<String> threeElement : threeElements) {
        System.out.println(threeElement.get(0) + " <"
                + threeElement.get(1) + ","
                + threeElement.get(2) + ">"
        );
    }
    // 输出到文件中
    try {
        BufferedWriter out = new BufferedWriter(new FileWriter(Config.lexiconResultPath));
        for (ArrayList<String> threeElement : threeElements) {
            out.write(threeElement.get(0) + " <"
                    + threeElement.get(1) + ","
                    + threeElement.get(2) + ">"
                    + "\n"
            );
        }
        out.close();
    } catch(IOException e) {
        throw new RuntimeException(e);
    }
    lex_result_stack = textLexicon.get_Lex_Result();
}
```

## 二、语法分析器设计

1. 解析文法，找到终结符和非终结符

2. 构造First集合

3. 构造Follow集合

4. 根据First集合和Follow集合构造预测表

5. 根据预测表和词法分析的结果进行语法分析


### 1. 解析文法

Formula 是表示文法的类，其中的left字段表示文法的左值，right表示文法的右值。有一个初始化方法，和两个gettr方法。

```python
class Formula:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def returnRights(self):
        return self.right

    def returnLeft(self):
        return self.left
}
```

TextParse 类是语法分析类，主要的工作就是根据语法规则来解析出语法分析需要的各种资源，包括文法，终结符，非终结符，First表，Follow表，预测表。

setFormulas() 这个方法用于从文法文件中解析出文法规则。解析的规则如下 left -> []right。具体代码如下：

```python
    def setFormulas():
        try:
            with open(Config.grammarPath, 'r') as file:
                for line in file:
                    if not line.strip():  # 检查是否为空白行
                        continue  # 跳过空白行
                    left, right = line.strip().split("->")
                    formula = Formula(left.strip(), right.strip().split(" "))
                    TextParse.formulas.append(formula)
        except Exception as e:
            print(e)
```

解析文法中的非终结符，并将其存储。因为文法中的非终结符就是文法左侧的全部符号，只需要统计左侧就可以了。

```python
    def setNonTerminals():
        # 解析文法中的非终结符
        for formula in TextParse.formulas:
            if formula.left not in TextParse.nonTerminals:
                TextParse.nonTerminals.append(formula.left)

```

解析文法中的终结符，并将其存储。文法中的终结符是文法中全部的符号去掉终结符。

```python
    def setTerminals():
        for formula in TextParse.formulas:
            rights = formula.returnRights()  # 在 Python 中，right 已经是一个列表
            for s in rights:
                if s not in TextParse.nonTerminals and s != "$":
                        TextParse.terminals.append(s)
```

### 2. 构造 First 集合

根据解析出的文法，终结符，非终结符来推导出 First 集合。根据以下算法来构造 First 集合。

```python
// 生成 First 集合
    def setFirsts():
        FirstTable.FirstTable.setFirst(TextParse.formulas, TextParse.terminals, TextParse.nonTerminals,
                                       TextParse.firsts)

```

- 使用 字典 来存储 First 集合，Key 值是符号，Value 值是元组 ，存储着 Key 的 First 集合中所有元素。

- 全部终结符号的 First 集合就是终结符本身。

- 将全部非终结符都注册一个字典，方便后序代码。

- 遍历文法右侧的每一个符号的First集合，然后将该符号的First集合去掉空加入到左侧文法的First集合中。这个过程就可以看作一个递归过程。


```python
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
```

### 3. 构造 Follow 集合

根据解析出的文法，终结符，非终结符。通过以下算法来推导出 Follow 集合。

```python
       def setFollows():
        FollowTable.FollowTable.setFollow(TextParse.formulas, TextParse.terminals, TextParse.nonTerminals,
                                          TextParse.firsts, TextParse.follows)

```

- 将文法开始符号 program 置于 Follow(program)。

- 将最后一个元素的 First 集合去掉空之后加入到文法右侧前一个元素的 Follow 集合中。

- 将文法左侧的 Follow 集合加入到文法右侧最后一个 First 集合中没有空的符号的 Follow 集合中。


```python
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

```

### 4. 构造预测表

```python
 def setPrediction():
        PredictMap.setPrediction(TextParse.formulas, TextParse.terminals, TextParse.nonTerminals, TextParse.firsts,
                                 TextParse.follows, TextParse.predictions)

```

- 遍历每一个文法

- 将文法左侧符号的 First 集合中的每一个终结符作为横坐标，左侧符号作为纵坐标，填上这个文法。

- 如果左侧文法符号的 First 集合中包含空，则将文法左侧的 Follow 集合的每一个终结符作为横坐标，左侧符号作为纵坐标，填上这个文法。


```python
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

```

### 5. 语法分析

- 根据上图来进行语法分析，不断的来进行移进规约。

- 首先要在压栈一个#，然后在输入串的末尾压入一个#

- 然后严格依照图中的遍历规则，来进行移进规约，直到 # 遇到 # 就结束。


```python
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

```

## 三、输出的一些表在文件的output文件夹中
