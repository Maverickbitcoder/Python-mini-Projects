import hashlib
import random

MODULUS = 97  # A small prime (in real cryptography this would be huge)
DIM = 4  # Small dimension for illustration

def vector_add(v1, v2):
    return [(a + b) % MODULUS for a, b in zip(v1, v2)]


def vector_scalar_mult(scalar, vector):
    return [(scalar * v) % MODULUS for v in vector]


def hash_function(message):
    # Simple hash using SHA-256
    digest = hashlib.sha256(message.encode()).digest()
    return int.from_bytes(digest, 'big') % MODULUS


# ----- KEY GENERATION -----
def keygen():
    # Secret key: random vector s1
    s1 = [random.randint(1, MODULUS - 1) for _ in range(DIM)]

    # Public matrix A and t = A * s1
    A = [[random.randint(1, MODULUS - 1) for _ in range(DIM)] for _ in range(DIM)]
    t = [sum((A[i][j] * s1[j]) % MODULUS for j in range(DIM)) % MODULUS for i in range(DIM)]

    return (A, t), s1


# ----- SIGNING -----
def sign(message, A, s1):
    # Random vector y
    y = [random.randint(1, MODULUS - 1) for _ in range(DIM)]

    # Compute A*y
    Ay = [sum((A[i][j] * y[j]) % MODULUS for j in range(DIM)) % MODULUS for i in range(DIM)]

    # Challenge value c = hash(Ay + message)
    c = hash_function(str(Ay) + message)

    # Compute z = y + c * s1
    cs1 = vector_scalar_mult(c, s1)
    z = vector_add(y, cs1)

    return (z, c)


# ----- VERIFICATION -----
def verify(message, A, t, z, c):
    # Compute A*z
    Az = [sum((A[i][j] * z[j]) % MODULUS for j in range(DIM)) % MODULUS for i in range(DIM)]

    # Compute c*t
    ct = vector_scalar_mult(c, t)

    # Recompute Ay' = Az - c*t
    Ay_prime = [(Az[i] - ct[i]) % MODULUS for i in range(DIM)]

    # Recompute challenge
    c_check = hash_function(str(Ay_prime) + message)

    return c_check == c

# 1. Key Generation
public_key, secret_key = keygen()
A, t = public_key
print("Secret key (s1):", secret_key)
print("Public key (A, t):")
for row in A:
    print("  ", row)
print("  t:", t)

# 2. Message to sign
message = "hello quantum world"
print("\nMessage:", message)

# 3. Sign the message
signature, challenge = sign(message, A, secret_key)
print("\nSignature (z):", signature)
print("Challenge (c):", challenge)

# 4. Verify the signature
valid = verify(message, A, t, signature, challenge)
print("\nSignature valid?", valid)