import random

n = int(input("Zadaj hody: "))
k = int(input("Zadaj kocky: "))

for i in range(n):
	sucet = 0
	for j in range(k):
		hod = random.randint(1, 6)
		sucet = sucet + hod
		print(f"Na kocke {j+1} padlo cislo {hod}")
	print(f"Dokopy padlo {sucet}.\n")