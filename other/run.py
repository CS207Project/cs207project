from pype import Pipeline

def pprint(p):
    for g in p.ir:
        print(p.ir[g].dotfile())
        #print(p.ir[g].topological_sort())

print("BASE")
p = Pipeline('tests/samples/six.ppl')
pprint(p)

# print("AE")
p.optimize_AssignmentEllision()
# pprint(p)

print("DCE")
p.optimize_DeadCodeElimination()
pprint(p)
