from pype.pipeline import Pipeline
from pype.parser import parser
from pype.lexer import lexer
from pype.translate import SymbolTableVisitor
import unittest

EXAMPLE_0_PATH = "tests/samples/example0.ppl"
EXAMPLE_0_TOKENS_PATH = "tests/samples/example0.tokens"

EXAMPLE_0_TOPO_PREOP = "['@N0', '@N1', '@N2', '@N5', '@N3', '@N4', '@N6', '@N7', '@N8']"
EXAMPLE_0_TOPO_AE = "['@N1', '@N6', '@N0', '@N7', '@N3', '@N8']"

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

    def test_compile(self):
         st = Pipeline(EXAMPLE_0_PATH)
         st.ir['standardize'].dotfile()

    def test_ae(self):
         st = Pipeline(EXAMPLE_0_PATH)
         st.optimize_AssignmentEllision()
         st.ir['standardize'].dotfile()


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
