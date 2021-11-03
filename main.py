from RSA import *
from elgamal import *

print("################")
print("# CRIPTOGRAPHY #")
print("################")
print("Choose Algorithm:")
print("1. RSA")
print("2. Elgamal")
print("----------------")
algoChosen = int(input("Input Algorithm Number: "))
print("")

if(algoChosen == 1):
    RSAMain()
elif(algoChosen == 2):
    ElgamalMain()