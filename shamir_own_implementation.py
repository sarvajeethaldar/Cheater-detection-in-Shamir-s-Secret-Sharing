# -*- coding: utf-8 -*-
"""
Created on Fri May  18 17:04:21 2020

@author: Sarva
"""
#from random import randint
#from lagrange import interpolate

from scipy.interpolate import lagrange
#from numpy.polynomial.polynomial import Polynomial

import random
import numpy as np





def generate_shares(n,k,p):



	s = float(input("Enter the secret(s) to be divide into shares such that s<p :"))

	#p=p_main
	#k=k_main
	#n=n_main

	"""Generating k-1 random numbers from a finite field of size p  """
	random_numbers = random.sample(range(1, p), k-1)#Using random.sample()
	#print(random_numbers)


	'''
	We are generating a polynomial of coeffients(aᵢ) for the polynomial such
	that aᵢ<p, p>s, p>n & a₀ = S
	'''
	random_numbers.append(s)
	poly = np.poly1d(random_numbers)
	print("Evaluating the polynomial at 0:", poly(0))



	'''
	We construct the n shares that are distributed to the participants. Each
	share is simply a point on the polynomial just defined.
	Each point D can be calculated in an iterative manner:
		Dx-1 =(x, f(x) mod p) where x=[1,2,....n]
		(Here we generate a list consisting of Dx-1 for all x in [1,2,...n])
	'''
	D=[]
	for i in range(1,n+1):
		Dy = poly(i) % p
		Dx = i
		Dxy = (Dx,Dy)
		D.append(Dxy)

	return D








def reconstruct_secret(X,Y,p):


	#In order to reconstruct the original secret from any k-out-of-n parts, we
	#need to recreate the polynomial that we defined in the beginning. This can
	#be achieved with the Lagrange Polynomial Interpolation.

	#X=X_main
	#Y=Y_main
	#p=p_main

	x = np.array(X)
	y = np.array(Y)
	poly = lagrange(x, y)

	#list_of_coefficients = Polynomial(poly).coef
	#poly = np.poly1d(list_of_coefficients)
	#s = Polynomial(poly).polyval(0, list_of_coefficients)
	s = poly(0) % p
	return s




#def reconstruct_secret(shares,p):
#	return interpolate(shares, p)














def main():
	"""Main function"""

	print("<<< Shamir's Secret Sharing Scheme >>>")
	print("Enter 1 to generate shares from a secret")
	print("Enter 2 to find the secret from keys")

	inp = int(input("Enter your value: "))


	if(inp == 1):


		'''Select a very large prime number(p) as the finite fields to which
		our algorthm will be restricted
		 '''
		p_main = 15485867
		print("Default Prime no.(p) for restricting finite fields: ", p_main )

		p_change = int(input("To change p enter a large prime else enter 0 :"))
		if(p_change!=0):
			p_main = p_change
			print("Prime no.(p) selected for restricting finite fields: ", p_main )


		#print("<<Enter integers only>>", end=" ")
		n_main = int(input("Enter the no. of shares(n) to be generated such that n<p :"))

		k_main = int(input("Enter the minimum no. of shares(k) required to reconstruct the secret:"))
		print("")
		print("<<< Publicly known values are >>>")
		print("No. of shares :",n_main)
		print("Threshold no. of shares :",k_main)
		print("Prime p:", p_main)

		D_main = generate_shares(n_main,k_main,p_main)
		print("The list of shares are:", D_main)




	elif(inp == 2):


		'''Select a very large prime number(p) as the finite fields to which
		our algorthm will be restricted
		 '''

		p_main = int(15485867)
		print("Default Prime no.(p) for restricting finite fields: ", p_main )

		p_change = int(input("To change p enter a large prime else enter 0 :"))
		if(p_change!=0):
			p_main = p_change
			print("Prime no.(p) selected for restricting finite fields: ", p_main )




		no_of_keys = int(input("Enter the no. of keys(max 20) :"))

		#this is because pol1d can't compute shares>20
		if(no_of_keys>20):
			print("Enter shares<=20")

		else:

			X_main=[]
			Y_main=[]
			#shares_main=[]
			for i in range(no_of_keys):

				print("Key",i+1, end=">>")

				X_main.append(float(input("Enter the x value of the key:")))
				Y_main.append(float(input("Enter the y value of the key:")))
			print("The secret is:", reconstruct_secret(X_main,Y_main, p_main))


'''
				x = float(input("Enter the x value of the key:"))
				y = float(input("Enter the y value of the key:"))
				xy= (x,y)
				shares_main.append(xy)

				print("The secret is:", reconstruct_secret(shares_main, p_main))
'''


if __name__ == '__main__':
    main()












