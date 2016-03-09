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
t_LPAREN = r'\)'
t_LBRACE = r'\['
t_RBRACE = r'\]'
t_OP_ADD = r'\+'
t_OP_SUB = r'-'
t_OP_MUL = r'\*'
t_OP_DIV = r'/'
t_STRING = r'\".*\"'
t_ASSIGN = r':='
t_NUMBER = r'\d'
#t_ID = r'\w+'

# TODO Ignore whitespace.
t_ignore = r'\s'
# TODO Write one rule for IDs and reserved keywords. Section 4.3 has an example.
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t
# TODO Ignore comments. Comments in PyPE are just like in Python. Section 4.5.

# TODO Write a rule for newlines that track line numbers. Section 4.6.

# TODO Write an error-handling routine. It should print both line and column numbers.

# This actually builds the lexer.
lexer = ply.lex.lex()
