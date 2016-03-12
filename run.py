from pype.pipeline import Pipeline

SymbolTable = Pipeline('bleh').compile(open('pype/samples/example1.ppl'))

SymbolTable.pprint()
