import random
from tsp import Chromosome


def rcx(parent_1, parent_2):
    def fill_with_parent1_genes(child, parent, genes_n):
        start_at = random.randint(0, len(parent.genes) - genes_n - 1)
        finish_at = start_at + genes_n
        for i in range(start_at, finish_at):
            child.genes[i] = parent_1.genes[i]

    def fill_with_parent2_genes(child, parent):
        j = 0
        for i in range(0, len(parent.genes)):
            if child.genes[i] is None:
                while parent.genes[j] in child.genes:
                    j += 1
                child.genes[i] = parent.genes[j]
                j += 1

    genes_n = len(parent_1.genes)
    child = Chromosome([None for _ in range(genes_n)])
    fill_with_parent1_genes(child, parent_1, genes_n // 2)
    fill_with_parent2_genes(child, parent_2)
    return child


def erx(parent_1, parent_2):
    n_len = len(parent_1)
    arr = [[0, 0] for _ in range(n_len)]
    visit = [False for _ in range(n_len)]
    for i in range(n_len):
        arr[parent_1[i]][0] = i
        arr[parent_2[i]][1] = i
    child = Chromosome([None for _ in range(n_len)])
    for i in range(n_len):
        if i == 0:
            child[i] = parent_1[random.randint(0, n_len - 1)]
        else:
            pos1 = arr[child[i - 1]][0]
            pos2 = arr[child[i - 1]][1]
            a, b = parent_1[(pos1 - 1 + n_len) % n_len], parent_1[(i + 1) % n_len]
            c, d = parent_2[(pos2 - 1 + n_len) % n_len], parent_1[(i + 1) % n_len]
            if not visit[a] and (a == c or a == d):
                child[i] = a
            elif not visit[b] and (b == c or b == d):
                child[i] = b
            elif not visit[c]:
                child[i] = c
            elif not visit[d]:
                child[i] = d
            else:
                a = 0
                while visit[a]:
                    a = random.randint(0, n_len - 1)
                child[i] = a
        visit[child[i]] = True
    return child


def cx2(parent_1, parent_2):
    n_len = len(parent_1)
    visit = [False for _ in range(n_len)]
    child = Chromosome([None for _ in range(n_len)])
    pos_map = [0 for _ in range(n_len)]
    for i in range(n_len):
        pos_map[parent_1[i]] = i
    child[0] = parent_2[0]
    visit[child[0]] = True
    for i in range(1, n_len):
        pos = pos_map[child[i - 1]]
        val = parent_2[pos]
        child[i] = parent_1[val]
    child.display()
    return child


def pmx(parent_1, parent_2):
    p1 = parent_1
    p2 = parent_2
    bcp = random.randint(0, len(p1) - 1)
    scp = random.randint(bcp + 1, len(p1))

    p1MiddleCross = p1[bcp:scp]
    p2MiddleCross = p2[bcp:scp]

    child1 = (p1[:bcp] + p2MiddleCross + p1[scp:])
    child2 = (p2[:bcp] + p1MiddleCross + p2[scp:])

    bd = []
    for i in range(len(p1MiddleCross)):
        bd.append([p2MiddleCross[i], p1MiddleCross[i]])

    b = []
    for pair in bd:
        for i in range(len(bd)):
            if pair[0] in bd[i] or pair[1] in bd[i]:
                if pair != bd[i]:
                    if pair[0] == bd[i][1]:
                        pair[0] = bd[i][0]
                    else:
                        pair[1] = bd[i][1]

        if pair not in b and pair[::-1] not in b:
            b.append(pair)

    for i in child1[:bcp]:
        for x in b:
            if i == x[0]:
                i = x[1]

    for i in child1[scp:]:
        for x in b:
            if i == x[0]:
                i = x[1]

    for i in child2[:bcp]:
        for x in b:
            if i == x[1]:
                i = x[0]

    for i in child2[scp:]:
        for x in b:
            if i == x[1]:
                i = x[0]

    return Chromosome(child2)

