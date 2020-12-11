def forgeBinary(number, size=32):
	return bin(number)[2:].zfill(size)[-size:] #zfill pour le padding et [-size:] pour s'assurer que le bloc 32 de taille

def rightRotation(number, offset=2 ,size=32):
	binNumber = forgeBinary(number, size)
	binNumber =  binNumber[-offset:]+binNumber[:-offset]
	return int(binNumber, 2)
def leftRotation(number, offset=1 ,size=32):
	binNumber = forgeBinary(number, size)
	binNumber =  binNumber[offset:]+binNumber[:offset]
	return int(binNumber, 2)

def addition_mod32(a, b):	
	return (a + b) % 4294967296

def divide_bitwise(number, size):
	blocks = []
	while number != 0:
		blocks.append(number & int('1'*size,2))
		number = number >>size
	return blocks
