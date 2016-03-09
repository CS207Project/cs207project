import ply.yacc

from .lexer import tokens,reserved
from .ast import *

# Here's an example production rule which constructs an AST node
def p_program(p):
  r'program : statement_list'
  p[0] = ASTProgram(p[1])

# Here's an example production rule which simply aggregates lists of AST nodes.
def p_statement_list(p):
  r'''statement_list : statement_list component
                     | statement_list import_statement
                     | import_statement
                     | component'''
  if len(p)>2:
    p[1].append(p[2])
    p[0] = p[1]
  else:
    p[0] = [p[1]]

# TODO Implement production rules for all other grammar rules and construct a
#      full AST.

# TODO
  r'import_statement : LPAREN IMPORT ID RPAREN'
# TODO
  r'''component : LBRACE ID expression_list RBRACE'''
# TODO
  r'''expression_list : expression_list expression
                      | expression'''
# TODO
  r'''expression : LPAREN INPUT declaration_list RPAREN
                 | LPAREN INPUT RPAREN'''
# TODO
  r'''expression : LPAREN OUTPUT declaration_list RPAREN
                 | LPAREN OUTPUT RPAREN'''
# TODO
  r'''declaration_list : declaration_list declaration
                       | declaration'''
# TODO
  r'''declaration : LPAREN type ID RPAREN
                  | ID'''
# TODO
  r'''type : ID'''
# TODO
  r'''expression : LPAREN ASSIGN ID expression RPAREN'''
# TODO
  r'''expression : LPAREN ID parameter_list RPAREN
                 | LPAREN ID RPAREN'''
# TODO
  r'''expression : LPAREN OP_ADD parameter_list RPAREN'''
# TODO
  r'''expression : LPAREN OP_SUB parameter_list RPAREN'''
# TODO
  r'''expression : LPAREN OP_MUL parameter_list RPAREN'''
# TODO
  r'''expression : LPAREN OP_DIV parameter_list RPAREN'''
# TODO
  r'''expression : ID'''
# TODO
  r'''expression : NUMBER'''
# TODO
  r'''expression : STRING'''
# TODO
  r'''parameter_list : parameter_list expression
                     | expression'''

# TODO: Write an error handling function. You should attempt to make the error
#       message sensible. For instance, print out the line and column numbers to
#       help find your error.
# NOTE: You do NOT need to write production rules with error tokens in them.
#       If you're interested, read section 6.8, but it requires a fairly deep
#       understanding of LR parsers and the language specification.
def p_error(p):

start = 'program'
parser = ply.yacc.yacc() # To get more information, add debug=True
