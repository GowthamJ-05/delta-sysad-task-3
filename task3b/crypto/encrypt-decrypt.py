from RSA_encrypt import RSA

rsa = RSA()
message = "Hello World"
cipher = rsa.encrypt(message)
print(rsa.privatekey)
print(rsa.publickey)

print(cipher)

decrypted_message = rsa.decrypt(cipher)
print(decrypted_message)

