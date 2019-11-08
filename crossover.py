import random
from tsp import Chromosome


def ox(parent_1, parent_2):
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


crossover = erx
