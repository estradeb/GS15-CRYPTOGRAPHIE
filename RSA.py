from SHA_1 import SHA_1

def compute_pgcd(a, b):
	while b != 0:
		a, b = b, a % b
	return a

def compute_lcm(x, y):
   lcm = (x*y)//compute_pgcd(x,y)
   return lcm

def is_coprime(a, b):
	return compute_pgcd(a, b) == 1

def init_alice():

	# 1
	print("Deux nombres copremiers ont déjà été stockés pour aller plus vite")
	p , q = 13332144011952475692844792665277339251038471684167210337080000835564590838277715004334349821463460988563502376804559805790138591307572695202210152239440283, 6666072005976237846422396332638669625519235842083605168540000417782295419138857502167174910731730494281751188402279902895069295653786347601105076119720141

	# 2
	n = p * q

	# 3
	lambda_n = compute_lcm(p - 1, q - 1)

	# 4
	""" A AMELIORER : 
		Choisir parmis que e des premiers aiderait pas mal
	"""
	for e in range(2, lambda_n):
		if is_coprime(e, lambda_n) :
			break
	# 5
	d = pow(e, -1, lambda_n)

	# n et e sont transmis à bob
	public_key = e , n 
	private_key = d, n
	return public_key, private_key

def text_signature(message, private_key):
	d, n = private_key
	Hash = SHA_1(message)
	return pow(Hash, d, mod=n)

def bob_signature_verification(unchecked_message, signature, public_key):
	e, n = public_key
	Hash = SHA_1(unchecked_message)
	if  pow(signature, e, mod=n) == Hash:
		print("message intacte !!!")
		return True
	else:
		print("message pas intacte")
		return False



# public_key, private_key = init_alice()

# signature = text_signature(message, private_key)

# print("signature = " , signature)

# bob_signature_verification(unchecked_message=message, signature=signature)

