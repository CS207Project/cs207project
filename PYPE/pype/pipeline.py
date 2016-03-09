from .lexer import lexer
from .parser import parser
from .ast import *
from .semantic_analysis import CheckSingleAssignment

class Pipeline(object):
  def __init__(self, source):
    self.compile(f)

  def compile(self, file):
    input = file.read()
    # Lexing, parsing, AST construction
    ast = parser.parse(input, lexer=lexer)
    # Semantic analysis
    ast.walk( CheckSingleAssignment() )

