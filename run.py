from tsp import *
import sys
import numpy
argument = sys.argv
if len(sys.argv) == 1:
    tsp_obj = TSP()
    tsp_obj.all_gen()
else:
    tsp_obj = TSP(filename=argument[1])
    data_table = [0.0 for _ in range(4)]
    time_table = [0.0 for _ in range(4)]
    repeation_count = 30
    for i in range(repeation_count):
        temp = tsp_obj.all_gen()
        for j in range(len(temp)):
            data_table[j] = data_table[j] + temp[j][0]
            time_table[j] = time_table[j] + temp[j][1]
    for j in range(len(temp)):
        data_table[j] = data_table[j] / repeation_count
        time_table[j] = time_table[j] / repeation_count

    f1 = open("experiment_data.txt", 'a')
    f2 = open("experiment_time.txt", 'a')
    s1 = argument[1]+" "
    s2 = argument[1]+" "
    for i in range(4):
        s1 = s1 + str(data_table[i]) + " "
        s2 = s2 + str(time_table[i]) + " "
    s1 = s1 + "\n"
    s2 = s2 + "\n"
    f1.write(s1)
    f2.write(s2)
    f1.close()
    f2.close()






