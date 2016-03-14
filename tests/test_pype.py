
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
