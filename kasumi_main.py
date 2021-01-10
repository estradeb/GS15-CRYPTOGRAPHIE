from chiffrement import *
from dechiffrement import *

f=open("texte_a_chiffrer.txt", "r")
if f.mode == 'r':
	content =f.read()

key = 'macron demissionne maintenant'
encrypted_content = kasumi_encrypt_CBC(content, key)


with open('texte_chiffré.txt', 'w') as f:
    f.write("%s\n" % encrypted_content)

decrypted_content = kasumi_decrypt_CBC(encrypted_content, key)
print( decrypted_content)
# with open('decrypted_content.txt', 'w') as f:
#     f.write("%s\n" % decrypted_content)
