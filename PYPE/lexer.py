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
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_OP_ADD = r'\+'
t_OP_SUB = r'-'
t_OP_MUL = r'\*'
t_OP_DIV = r'/'
t_STRING = r'\".*\"'
t_ASSIGN = r':='
t_NUMBER = r'\d+'
#t_ID = r'\w+'

# Ignore whitespace.
t_ignore = ' \t\r\f\v'

# Write one rule for IDs and reserved keywords. Section 4.3 has an example.
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Ignore comments. Comments in PyPE are just like in Python. Section 4.5.
def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

# Write a rule for newlines that track line numbers. Section 4.6.
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Write an error-handling routine. It should print both line and column numbers.
# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) - 1
    return column

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0],"in line {}".format(t.lineno) , "and column {}".format(find_column(t.lexer.lexdata, t)))
    t.lexer.skip(1)
    #print(vars(t.lexer)['lexdata'])

# This actually builds the lexer.
lexer = ply.lex.lex()

""" commented 3/10 by DNY
# Test it out
data = '''
3 + 4 * 10
  + -20 *2 + a
^
'''
# Give the lexer some input
lexer.input(data)

print(vars(lexer).keys())

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
    print(type(tok.value))
    print(tok.type)
"""
