from DNF import DFA
from Lexer import Lexer
from NFA import NFA
from Readtxt import ReadTXT
from TokenTable import TokenTable


def do(file):
    input_file = file
    output_file = "D:\python\pythonProject\output\\file"

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
