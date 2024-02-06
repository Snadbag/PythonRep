import random

n = int(input("Zadaj n: "))
p = 100 # passengers

for i in range(n):
	vystupi = random.randint(0, 9)
	nastupi = random.randint(0, 9)
	zostalo = p + nastupi - vystupi

	print(f"Vo vlaku bolo {p} ludi, nastupilo {nastupi}, vystupilo {vystupi} a zostalo {zostalo}.")
	p = zostalo