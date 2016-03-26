from pype import Pipeline

p = Pipeline('../tests/samples/example0.ppl')
assert p.ir['standardize'].dotfile()
print(p.ir['standardize'].topological_sort())

p.optimize_AssignmentEllision()
print(p.ir['standardize'].dotfile())
print(p.ir['standardize'].topological_sort())
