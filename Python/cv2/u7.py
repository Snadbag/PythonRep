def rectangle(w, symbol = "*"):
	print(symbol * w)
	print(symbol + ((w - 2) * " ") + symbol)
	print(symbol * w)

rectangle(8, "H")