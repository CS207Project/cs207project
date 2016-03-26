from .lexer import lexer
from .parser import parser
from .ast import *
from .semantic_analysis import CheckSingleAssignment, CheckSingleIOExpression, CheckUndefinedVariables
from .translate import SymbolTableVisitor, LoweringVisitor
from .optimize import AssignmentEllision

class Pipeline(object):
    def __init__(self, source):
        with open(source) as f:
            self.ir = self.compile(f)

    def compile(self, file):
        input = file.read()

        # Lexing, parsing, AST construction
        ast = parser.parse(input, lexer=lexer)

        # Semantic analysis
        ast.walk( CheckSingleAssignment() )
        ast.walk( CheckSingleIOExpression() )
        syms = ast.walk( SymbolTableVisitor() )
        ast.walk( CheckUndefinedVariables(syms) )

        # Translation
        ir = ast.mod_walk( LoweringVisitor(syms) )

        return ir

    def optimize_AssignmentEllision(self):
        self.ir.flowgraph_pass( AssignmentEllision() )

    def optimize_DeadCodeElimination(self):
        # ir.flowgraph_pass( DeadCodeElimination() )
        pass

    def optimize(self):
        # Optimization
        optimize_AssignmentEllision()
        optimize_DeadCodeElimination()
