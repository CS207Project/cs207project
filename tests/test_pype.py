from pype.pipeline import Pipeline
from pype.parser import parser
from pype.lexer import lexer
from pype.translate import SymbolTableVisitor
import unittest

EXAMPLE_0_PATH = "tests/samples/example0.ppl"
EXAMPLE_0_TOKENS_PATH = "tests/samples/example0.tokens"

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


#SymbolTable = Pipeline('bleh').compile(open('pype/samples/example1.ppl'))

#SymbolTable.pprint()


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
