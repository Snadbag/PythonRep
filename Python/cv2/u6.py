n = int(input("Zadaj n: "))

while n != 1:
	if (n % 2 == 0):
		n = n // 2
	else:
		n = n * 3 + 1
	if n == 1: print(f"{n}", end="")
	else: print(f"{n}", end=",\u0020")