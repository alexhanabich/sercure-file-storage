import random

# fast mod exp (proof on)
def mod_exp(g, a, p):
    r = 1
    y = g%p
    while a > 0:
        if a&1 == 1:
            r = (r*y) % p
        y = y**2 % p
        a >>= 1
    return r

def miller_rabin(n,k):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n-1)
        x = mod_exp(a, s, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(r-1):
            x = mod_exp(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True


def generate_prime(prime_bit):
    low = pow(2, prime_bit-1)
    high = pow(2, prime_bit)-1
    cnt = 0
    while True:
        rand_num = random.getrandbits(prime_bit)
        while rand_num not in range(low, high+1) or not rand_num%2:
            rand_num = random.getrandbits(prime_bit)
        if miller_rabin(rand_num, 64):
            return rand_num


# if xa + yb = 1
# then xa = 1 mod b (mod b removes all multiples of b)
# then x = a^(-1) mod b
# using an adaptation of egcd
def mult_inv(a, n):
    t, newt = 0 ,1
    r, newr = n, a
    while newr != 0:
        q = r//newr
        t, newt = newt, t-q*newt
        r, newr = newr, r-q*newr
    if r > 1:
        raise Exception('not invertible')
    return t%n


# based on the theorm that gcd(a,b) = gcd(b,a%b)
def gcd(a,b):
    while b > 0:
        a,b = b, a % b
    return a