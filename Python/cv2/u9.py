import random

n = int(input("Zadaj n: "))

matica = [[] for _ in range(n)]

for i in range(n):
	for j in range(n):
		matica[i].insert(j, random.randint(1, 9))
print(matica)

def sort(n):   
	new = matica[n]
	temp = [new] + matica[0:n] + matica[n+1:]
	return temp

for i in range(1, n):
	matica = sort(i)
	print(matica)
