
import random

cr = round(random.uniform(0.2, 0.9), 2)
while (cf:=round(random.uniform(0.1, 0.9), 2)) >= cr: pass
while (ci:=round(random.uniform(0.1, 0.9), 2)) >= cr: pass
while (ci:=round(random.uniform(0.1, 0.9), 2)) >= cf: pass
er = round(random.uniform(0.2, 0.9), 2)
while (ef:=round(random.uniform(0.1, 0.9), 2)) >= er: pass


N = list(range(1, 50))
K = list(range(len(N), len(N) + 50))
M = list(range(len(N + K), len(N + K) + 20))
O = list(range(1, 10))

pontos = N + K + M

b = {}
for o in O:
    b[o] = random.randint(1, 5000)

a = {}
for i in N:
    a[i] = sum(b.values()) if random.random() <= 0.3 else random.randint(100, 100000)
    
CF = {}
for k in K:
    CF[k] = sum(b.values()) if random.random() <= 0.3 else random.randint(500, 5000)

CP = {}
for j in M:
    CP[j] = sum(b.values()) if random.random() <= 0.3 else random.randint(1000, 5000)

D = {}
for x in pontos:
    D[x] = [round(random.uniform(1.0, 600.0), 4), round(random.uniform(1.0, 600.0), 4)]

with open("instances.txt", "w") as file:
    file.write(str(cr) + "\n" + str(cf) + "\n" + str(ci) + "\n" + str(er) + "\n" + str(ef))
    file.write("\n" + str(len(N)) + "\n" + str(len(K)) + "\n" + str(len(M)) + "\n" + str(len(O)) + "\n")
    
    for o in O:
        file.write(str(b[o]) + " ")
    
    file.write("\n")
    
    for i in N:
        file.write(str(a[i]) + " ")
    
    file.write("\n")
    
    for k in K:
        file.write(str(CF[k]) + " ")
        
    file.write("\n")
    
    for j in M:
        file.write(str(CP[j]) + " ")
    
    file.write("\n")
    
    for x in pontos:
        file.write(str(x) + " " + str(D[x][0]) + " " + str(D[x][1]) + "\n")