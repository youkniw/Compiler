from DNF import DFA
from Lexer import Lexer
from MainParse import MainParse
from NFA import NFA
from Readtxt import ReadTXT
from TokenTable import TokenTable


def do():
    input_file = "D:\python\pythonProject\input\\1.txt"
    output_file = "D:\python\pythonProject\\file"
    # Reading the input file
    content = ReadTXT.read_txt(input_file)  # Assuming read_txt is a function from ReadTxt class
    # Initializing NFA, DFA, and TokenTables
    nfa = NFA()
    dfa = DFA(nfa)
    dfa.convertNFAToDFA()
    dfa.minimizeDFA()
    token_table1 = TokenTable()
    token_table2 = TokenTable()
    # Running the lexer
    lexer = Lexer(content, token_table1, token_table2, dfa)
    lexer.run()
    # Outputting the results
    token_table1.printTokenTable()
    token_table2.saveTokenTable(output_file)



if __name__ == "__main__":

    do()
    MainParse.DoParse()  # 执行语法分析
