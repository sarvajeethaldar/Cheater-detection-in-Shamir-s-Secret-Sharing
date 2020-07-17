# -*- coding: utf-8 -*-
"""
Created on Wed May  27 23:29:42 2020

@author: Sarva
"""

import random
import math

#%%

# Helper function
def isprime(n):
    if n == 2:
       return True
    if n == 1 or n % 2 == 0:
        return False
    i = 3
    while i <= math.sqrt(n):
        if n % i == 0:
            return False
        i = i + 2
    return True

#%%
print("<<< Feldman's Verifiable Secret Sharing Scheme >>>")


# Pick q, p primes such that q | p - 1, that is equvalent to
# say that p = r*q + 1 for some r

# Choose q
while True:
    q = 127 #int(input("Insert a prime q: "))
    if isprime(q):
        break

print("\n\n<<< Choosing primes >>>")
print("\nq is the prime, ", end='')
print("q = " + str(q))


#%%


# Find p and r
r = 1
while True:
    p = r*q + 1
    if isprime(p):
        print("\nr = " + str(r))
        print("p is prime, ", end="")
        print("p = " + str(p))
        break
    r = r + 1




#%%

# Compute elements of Z_p*
Z_p_star = []
for i in range(0, p):
    if(math.gcd(i,p) == 1):
        Z_p_star.append(i)

print("\n\n<<< Generating cyclic group >>>")
print("\nZ_p* = ")
print(Z_p_star)



#%%

# Compute elements of G = {h^r mod p | h in Z_p*}
G = []
for i in Z_p_star:
    G.append(i**r % p)

G = list(set(G))
G.sort()

print("\nG = ")
print(G)
print("\nOrder of G is " + str(len(G)) + ". This must be equal to q.")


#%%


# Since the order of G is prime, any element of G except 1 is a generator
g = random.choice(list(filter(lambda g: g != 1, G)))
print("g = " + str(g))
print("G is the cyclic group which is generated by g")
# Secret taken from the group Z_q*
while True:
    a0 = 84 #int(input("Inser a secret in Z_q*: "))
    if a0 >= 1 or a0 <= q:
        break


#%%


# Secret polynomial coefficients taken from the group Z_q*
a1 = random.randint(1, q)
a2 = random.randint(1, q)

a = [a0, a1, a2]

print("\nLet the secret polynomial be: " + str(a0) + " + " +  str(a1) + "x + " + str(a2) + "x^2")
print("(Secret polynomial coefficients taken from the group Z_q)")


#%%

# The function f is a polynomial from the group Z_q* (for simplicity 2nd degree is considered)
def f(x):
    return ((a0 + a1*x + a2*x**2) % q)

# List of shares
s = []



print("\n\n<<< Computing shares and verifying them >>>")

# Compute shares and verify
# Note that P_i receives as a share s = f(i)
# In general, each party P_1,...,P_6 could receive a different arbitrary share
for i in range(1,7):
    print("\ni = " + str(i))
    s.append(f(i))
    print("Share: f(" + str(i) + ") = " + str(f(i)))
    print("Commitment: g^f(" + str(i) + ") = " + str(g**f(i) % p))
    print("Verification: (g^a0)*((g^a1)^i)*((g^a2)^(i^2)) = " + str((g**a0)*((g**a1)**i)*((g**a2)**(i**2)) % p) + "\n")





# Print shares
print("The list of shares are:", end=" ")
print(s)


#%%

# Parties cooperating to reconstruct the secret
B = [1,2,3]

def delta(i):
    d = 1
    print("i= "+str(i))
    #print(i)
    for j in B:
        if j != i:
            print("j= "+str(j))
            #print(j)
            d *= -j/(i - j)
    print("delta = " + str(d % q))
    return d

print("\n\n<<< Reconstructing the secret >>>")

a0_reconstructed = 0
for i in B:
    print("\nShare of P_" + str(i) + " is " + str(s[i - 1]))
    a0_reconstructed += delta(i)*s[i - 1]

print("\nThe secret is: " + str(a0_reconstructed % q))
