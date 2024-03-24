import rsa
import sympy
import random

def generate_primes():
    lower = pow(2,128)
    upper = 1000*lower
    p,q=0,0
    p=sympy.randprime(lower,upper)
    q=sympy.randprime(lower,upper)
    while q==p:
        q=sympy.randprime(lower,upper)
    return (p,q)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


def generate_keypair(p, q):

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = multiplicative_inverse(e, phi)

    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)

def callable():
    p, q = generate_primes()
    public_key, private_key = generate_keypair(p, q)
    return public_key, private_key
# print (public_key, private_key)

# message = "Hello, World!"
# print (public_key, private_key)
# encrypted_message = encrypt(public_key, message)
# decrypted_message = decrypt(private_key, encrypted_message)

# print("Original message:", message)
# print("Encrypted message:", encrypted_message)
# print("Decrypted message:", decrypted_message)