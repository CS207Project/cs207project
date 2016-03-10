import ply.yacc

from lexer import tokens,reserved
from ast import *

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
    p[0] = p[1] + [p[2]]
  else:
    p[0] = [p[1]]

def p_import_statement(p):
  r'import_statement : LPAREN IMPORT ID RPAREN'
  p[0] = ASTImport(p[4])

def p_component(p):
  r'''component : LBRACE ID expression_list RBRACE'''
  p[0] = ASTComponent(ASTID(p[2]),p[3])

def p_expression_list(p):
  r'''expression_list : expression_list expression
                      | expression'''
  if len(p) > 2:
    p[0] = p[1] + [p[2]]
  else:
    p[0] = [p[1]]

def p_input(p):
  r'''expression : LPAREN INPUT declaration_list RPAREN
                 | LPAREN INPUT RPAREN'''
  if len(p) > 4:
    p[0] = ASTInputExpr(p[3])
  else:
    p[0] = ASTInputExpr([])

# returns ASTOutputExpr
def p_output(p):
  r'''expression : LPAREN OUTPUT declaration_list RPAREN
                 | LPAREN OUTPUT RPAREN'''
  if len(p) > 4:
    p[0] = ASTOutputExpr(p[3])
  else:
    p[0] = ASTOutputExpr([])

# returns [ASTID, ... ]
def p_declaration_list(p):
  r'''declaration_list : declaration_list declaration
                       | declaration'''
  if len(p) > 2:
    p[0] = p[1] + [p[2]]
  else:
    p[0] = [p[1]]

# returns ASTID
def p_declaration(p):# not sure I did this one correctly
  r'''declaration : LPAREN type ID RPAREN
                  | ID'''
  if len(p) > 2:
    p[0] = ASTID(p[3],typedecl=p[2])
  else:
    p[0] = ASTID(p[1])

# return the name of the type
def p_type(p):
  r'''type : ID'''
  p[0] = p[1] # // do not wrap in ASTID, will be done later in p_declaration()

# return ASTAssignmentExpr
def p_assign(p):
  r'''expression : LPAREN ASSIGN ID expression RPAREN'''
  p[0] = ASTAssignmentExpr(ASTID(p[3]),p[4])

# return ASTEvalExpr
def p_functioncall(p):
  r'''expression : LPAREN ID parameter_list RPAREN
                 | LPAREN ID RPAREN'''
  # convert ID into ASTID
  if len(p) > 3:
    p[0] = ASTEvalExpr(ASTID(p[2]),p[3])
  else:
    p[0] = ASTEvalExpr(ASTID(p[2]), [] ) # pass in empty arguments

# return ASTEvalExpr
def p_operator(p):
  r'''expression : LPAREN OP_ADD parameter_list RPAREN
                 | LPAREN OP_SUB parameter_list RPAREN
                 | LPAREN OP_MUL parameter_list RPAREN
                 | LPAREN OP_DIV parameter_list RPAREN '''
  p[0] = ASTEvalExpr(ASTID(p[2]),p[3])

""" ignoring through combination in p_operator (see examples)
  r'''expression : LPAREN OP_SUB parameter_list RPAREN'''
  r'''expression : LPAREN OP_MUL parameter_list RPAREN'''
  r'''expression : LPAREN OP_DIV parameter_list RPAREN'''
"""

def p_identification(p):
  r'''expression : ID'''
  p[0] = ASTID(p[1])

def p_literal(p):
  r'''expression : NUMBER
                 | STRING'''
  p[0] = ASTLiteral(p[1])

""" combine in p_literal
  r'''expression : STRING'''
"""

def p_parameter_list(p):
  r'''parameter_list : parameter_list expression
                     | expression'''
  if len(p) > 2:
    p[0] = p[1]+ [p[2]]
  else:
    p[0] = [p[1]]

# TODO: Write an error handling function. You should attempt to make the error
#       message sensible. For instance, print out the line and column numbers to
#       help find your error.
# NOTE: You do NOT need to write production rules with error tokens in them.
#       If you're interested, read section 6.8, but it requires a fairly deep
#       understanding of LR parsers and the language specification.
def p_error(p): #TODO
  print("\n\n")
  print("error occured")
  print(p)
  print(vars(p).keys())
  print("\n\n")
  #p.parser.skip(1) figure out how to skip token

start = 'program'
parser = ply.yacc.yacc() # To get more information, add debug=True

# test out the program
"""
from lexer import lexer

data = '''
(import timeseries)

{ standardize
  (:= new_t (/ (- t mu) sig))
  (:= mu (mean t))
  (:= sig (std t))

  (input (TimeSeries t))
  (output new_t)
}
'''

# Give the lexer some input
ast = parser.parse(data, lexer=lexer)
ast.pprint()
"""
