import tsplib95 as tsp
from haversine import haversine


# x = tsp.load_problem("ali535.tsp")

def read_tsp_data(tsp_name):
    tsp_name = tsp_name
    with open(tsp_name) as f:
        content = f.read().splitlines()
        cleaned = [x.lstrip() for x in content if x != ""]
        lst = []
        for s in cleaned:
            if '0' <= s[0] <= '9':
                _, first_cord, second_cord = re.split('\ +', s)
                lst.append((float(first_cord), float(second_cord)))
        return lst


# x=read_tsp_data("ali535.tsp")
# print(haversine(x[0][0],x[0][1]))

f1 = open("experiment_time.txt", "r")
data = []
s1 = f1.readline()
data = s1.split(" ")
f1.close()
f1 = open("experiment_time.txt", "w")
for i in range(1, 5):
    data[i] = (float(data[i]) * 1000) / 200
s1 = ""
for i in range(5):
    s1 += str(data[i]) + " "
s1 += "\n"
f1.write(s1)
f1.close()
