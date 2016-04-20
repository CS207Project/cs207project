from pype.pipeline import Pipeline
from pype.parser import parser
from pype.lexer import lexer
from pype.translate import SymbolTableVisitor
import unittest

EXAMPLE_0_PATH = "tests/samples/example0.ppl"
EXAMPLE_0_TOKENS_PATH = "tests/samples/example0.tokens"
EXAMPLE_SIX_PATH = "tests/samples/six.ppl"
EXAMPLE_ICvisit_PATH = "tests/samples/icvisit.ppl"

EXAMPLE_0_TOPO_PREOP = "['@N0', '@N1', '@N2', '@N5', '@N3', '@N4', '@N6', '@N7', '@N8']"
EXAMPLE_0_TOPO_AE = "['@N1', '@N6', '@N0', '@N7', '@N3', '@N8']"

def pprint(p):
    for g in p.ir:
        print(p.ir[g].dotfile())
        print(p.ir[g].topological_sort())

class PYPYTests(unittest.TestCase):

    def test_lexing(self):
        lexer.input(open(EXAMPLE_0_PATH).read())
        expOut = open(EXAMPLE_0_TOKENS_PATH)

        for tok,line in zip(lexer,expOut):
            self.assertEqual(str(tok),line.strip())

    def test_parsing(self):
        inp = open(EXAMPLE_0_PATH).read()
        ast = parser.parse(inp,lexer=lexer)
        syms = ast.walk( SymbolTableVisitor() )
        syms.pprint()

    def test_pipeline(self):
        p = Pipeline(EXAMPLE_0_PATH)
        pprint(p)

        p.optimize_AssignmentEllision()
        pprint(p)

        p.optimize_DeadCodeElimination()
        pprint(p)

    def test_opt(self):
        p = Pipeline(EXAMPLE_SIX_PATH)
        p.optimize()
        self.assertEqual(len(p.ir['six'].nodes),4)

    def test_ICvisit(self):
         p = Pipeline(EXAMPLE_ICvisit_PATH)
         #p.ir.topological_flowgraph_pass( InlineComponents() )



# test out the program
"""
from .lexer import lexer

data = '''
(import timeseries)
{ blah
(:= t 4)
}
'''

'''
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
