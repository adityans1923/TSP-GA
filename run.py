from tsp import *
import sys
argument = sys.argv
if len(sys.argv) == 1:
    tsp_obj = TSP()
    tsp_obj.all_gen()
else:
    tsp_obj = TSP(filename=argument[1])
    tsp_obj.all_gen()



