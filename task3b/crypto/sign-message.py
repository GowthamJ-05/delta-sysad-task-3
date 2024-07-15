from RSA_encrypt import RSA
import hashlib
rsa = RSA()

message_to_send = "Hello World"
encrypted_message = rsa.encrypt(message_to_send)
private_key = rsa.privatekey
public_key = rsa.publickey
print("Encrypted Message: ", encrypted_message)

signed_message = rsa.sign(message_to_send)
print("Signed Message: ", signed_message)


# the encrypted_message and signed_hash_message are sent
# and received by the other user having the private key

message_received = encrypted_message
signed_message_received = signed_message
rsa2 = RSA()
hash_sign_message = rsa2.reverse_sign(signed_message_received, public_key['n'], public_key['e'])


rsa2 = RSA()
decrypted_message = rsa2.decrypt(message_received, private_key['n'], private_key['d'])
hash_decrypted_message = hashlib.sha256(decrypted_message.encode("utf-8")).hexdigest()

if hash_sign_message == hash_decrypted_message:
    print("The message is signed and is from a verified source")
else:
    print("The message source is unknown")
