import base64

def base64_encode(message):
	message_bytes = message.encode('ascii')
	base64_bytes = base64.b64encode(message_bytes)
	return base64_bytes.decode('ascii')
def base64_decode(base64_message):
	base64_bytes = base64_message.encode('ascii')
	message_bytes = base64.b64decode(base64_bytes)
	return message_bytes.decode('ascii')



a = "bonjour je m'appelle benoit"

b = base64_encode(a)
print(b)
print(base64.decodebytes(b))
c = base64_decode(b)
print(c)
