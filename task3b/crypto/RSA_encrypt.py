import math
import random
import hashlib

class RSA:
    def __init__(self):

        self.prime1 = None
        self.prime2 = None
        self.primelist = list()
        self.message_to_accept = None
        self.cipher_to_return = None
        self.e = None
        self.d = None
        self.n = None
        self.privatekey = None
        self.publickey = None

        # self.message_to_return = None
        # self.cipher_to_accept = None


    def encrypt(self, message):
        self.message_to_accept = message.encode('utf-8')

        self._assign_primes(250)

        self._assign_keys()
        self.publickey = {'e': self.e, 'n': self.n}
        self.privatekey = {'d': self.d, 'n': self.n}

        self._assign_cipher()

        return self.cipher_to_return

    def _assign_primes(self, upper_limit):
        sieve = [False] * 2 + [True] * (upper_limit-1)
        range_to_search = int(math.sqrt(upper_limit))
        for i in range(2, range_to_search+1):
            j = 1
            while i * j <= upper_limit:
                sieve[i*j] = False
                j += 1
        for index in range(len(sieve)):
            if sieve[index]:
                self.primelist.append(index)

        self.primelist = self.primelist[5:]  # to remove the primes up to 13. The product of the primes must atleast be > 256 for encoding

        self.prime1 = self.primelist[random.randint(0, len(self.primelist)-1)]
        self.primelist.remove(self.prime1)
        self.prime2 = self.primelist[random.randint(0, len(self.primelist)-1)]

    def _assign_keys(self):

        self.n = self.prime1 * self.prime2
        phi = (self.prime1-1) * (self.prime2-1)
        self._assign_e(phi)
        self._assign_d(phi)

    def _assign_e(self, phi):
        while True:
            self.e = random.randint(3, phi-1)
            if self._gcd(self.e, phi) == 1:
                break

    def _gcd(self, a, b):
        if a > b:
            if b == 0:
                return a
            return self._gcd(b, a % b)
        else:
            return self._gcd(b, a)

    def _assign_d(self, phi):
        gcd, so, to = self._egcd(self.e, phi)
        if so < 0:
            self.d = phi + so
        else:
            self.d = phi + so

    def _egcd(self, a, b):
        so, to = 0, 1
        sn, tn = 1, 0
        while a != 0:
            quotient, remainder = b // a, b % a
            sn_temp = so - sn*quotient
            tn_temp = to - tn*quotient
            b, a, so, to, sn, tn = a, remainder, sn, tn, sn_temp, tn_temp
        gcd = b
        return gcd, so, to


    def _assign_cipher(self):
        self.cipher_to_return = list()
        for byte in self.message_to_accept:
            # c = pow(byte, self.e, self.n)
            c = 1
            e1 = 0
            while e1 < self.e:
                e1 += 1
                c = (c * byte) % self.n
            self.cipher_to_return.append(c)


    def decrypt(self, cipher, n=None, key=None):

        if key is None:
            key = self.d

        if n is None:
            n = self.n

        message_to_return = list()
        for char in cipher:
            # c = pow(char, self.d, self.n)
            c = 1
            d = 0
            while d < key:
                d += 1
                c = (c * char) % n
            message_to_return.append(c.to_bytes(1, "little").decode("utf-8"))

        return ''.join(char for char in message_to_return)

    def sign(self, message, n=None, key=None):
        if n is None:
            n = self.n
        if key is None:
            key = self.d

        hashed_value = hashlib.sha256(message.encode('utf-8')).hexdigest().encode('utf-8')

        signed_message = list()

        for byte in hashed_value:
            c = 1
            d = 0
            while d < key:
                d += 1
                c = (c * byte) % n
            signed_message.append(c)

        return signed_message


    def reverse_sign(self, signed_message, n=None, key=None):

        if n is None:
            n = self.n
        if key is None:
            key = self.e

        message_to_return = list()

        for char in signed_message:
            c = 1
            e = 0
            while e < key:
                e += 1
                c = (c * char) % n
            message_to_return.append(c.to_bytes(1, "little").decode("utf-8"))

        return ''.join(char for char in message_to_return)


# If the self.n had been sufficiently large, (> 256 bits) then below functions define sign and reverse_sign
'''
    def sign(self, message, n=None, key=None):
        if n is None:
            n = self.n
        if key is None:
            key = self.d

        hashed_value = int(hashlib.sha256(message.encode('utf-8')).hexdigest(),16)

        c = 1
        d = 0
        while d < key:
            d += 1
            c = (c * hashed_value) % n

        return c
    
    def reverse_sign(self, signed_message, n=None, key=None):
    
        if n is None:
            n = self.n
        if key is None:
            key = self.e
    
    
        c = 1
        e = 0
        while e < key:
            e += 1
            c = (c * signed_message) % n
    
        return c
        
'''