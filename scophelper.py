def count(file): 
    with open(file, 'r') as f: 
        scop_count = 0
        for line in f: 
            if '#pragma scop' in line:  # fix
                scop_count += 1
    return scop_count

def get(file):
    with open(file, 'r') as f: 
        scops = []
        scop = []
        inscop = False
        for line in f: 
            if '#pragma scop' in line:  # fix
                scop.append(line)
                inscop = True
            elif '#pragma endscop' in line:  # fix
                scop.append(line)
                scops.append(scop)
                scop = []
                inscop = False
            elif inscop: 
                scop.append(line)
    return scops
