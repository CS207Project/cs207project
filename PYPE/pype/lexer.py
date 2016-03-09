import ply.lex

reserved = { # pattern : token-name
  'input' : 'INPUT',
  'output' : 'OUTPUT',
  'import' : 'IMPORT',
}
# 'tokens' is a special word in ply's lexers.
tokens = [ 
  'LPAREN','RPAREN', # Individual parentheses
  'LBRACE','RBRACE', # Individual braces
  'OP_ADD','OP_SUB','OP_MUL','OP_DIV', # the four basic arithmetic symbols
  'STRING', # Anything enclosed by double quotes
  'ASSIGN', # The two characters :=
  'NUMBER', # An arbitrary number of digits
  'ID', # a sequence of letters, numbers, and underscores. Must not start with a number.
] + list(reserved.values())

# TODO You'll need a list of token specifications here.
# TODO Here's an example:
t_LPAREN = r'\('
t_LPAREN
t_RPAREN
t_LBRACE
t_RBRACE
t_OP_ADD
t_OP_SUB
t_OP_MUL
t_OP_DIV
t_STRING
t_ASSIGN
t_NUMBER
t_ID

# TODO Ignore whitespace.

# TODO Write one rule for IDs and reserved keywords. Section 4.3 has an example.

# TODO Ignore comments. Comments in PyPE are just like in Python. Section 4.5.

# TODO Write a rule for newlines that track line numbers. Section 4.6.

# TODO Write an error-handling routine. It should print both line and column numbers.

# This actually builds the lexer.
lexer = ply.lex.lex()
