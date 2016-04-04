from pype import Pipeline
from timeseries import TimeSeries
# // Akhil's code for testing Assignment Ellision and DeadCodeElimination (DNY Comment)
# def pprint(p):
#     for g in p.ir:
#         print(p.ir[g].dotfile())
#         #print(p.ir[g].topological_sort())
#
# print("BASE")
# p = Pipeline('tests/samples/six.ppl')
# pprint(p)
#
# # print("AE")
# p.optimize_AssignmentEllision()
# # pprint(p)
#
# print("DCE")
# p.optimize_DeadCodeElimination()
# pprint(p)
t = TimeSeries(list(range(10)),list(range(10)))
pipeline = Pipeline('../tests/samples/example0.ppl')
value = pipeline['standardize'].run(t)
print(repr(value))
