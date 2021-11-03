from math import gcd
import random

class Paillier:
    def __init__(self):
        pass

    def generate_keys(self):
        print("Generating paillier keys...")
        with open("primes.txt", "r") as f:
            primes = [int(prime) for prime in f.read().strip().replace("  ", " ").split('\n')]
            primes = primes[0:200]
        p = random.choice(primes)
        q = random.choice(primes)
        while (gcd(p*q, (p-1)*(q-1)) != 1):
            p = random.choice(primes)
            q = random.choice(primes)
        n = p*q
        lcm = int(abs((p-1)*(q-1)) / gcd(p-1,q-1))
        g = random.randint(1, (n**2)-1)
        x = (g**lcm) % (n**2)
        lx = (x-1)/n
        myu = self.mod_inverse(lx, n)
        self.g, self.n, self.lcm, self.myu = g, n, lcm, myu
        f_public = open('publicKey.pub', 'w')
        f_public.write(str(g) + ', ' + str(n))
        f_public.close()
        f_private = open('privateKey.pri', 'w')
        f_private.write(str(lcm) + ', ' + str(myu))
        f_private.close()
        # print(self.g, self.n, self.lcm, self.myu)

    def mod_inverse(self, lx, n):
        for x in range(1, n):
            if (((lx%n) * (x%n)) % n == 1):
                return x
        return -1
    
    def encrypt(self, plaintext):
        print("Encrypting...")
        ciphertext = []
        r = random.randint(0,self.n-1)
        while (gcd(r,self.n-1) != 1):
            r = random.randint(0,self.n-1)
        for x in plaintext:
            m = ord(x)
            c = ((self.g**m) * (r**self.n)) % (self.n ** 2)
            ciphertext.append(c)
        print("Success!")
        return ciphertext
    
    def decrypt(self, ciphertext):
        print("Decrypting...")
        ciphertext = list(map(int, ciphertext.split(",")))
        plaintext = []
        for c in ciphertext:
            x = ((c ** self.lcm) % (self.n ** 2))
            lx = (x-1)/self.n
            m = (lx * self.myu) % (self.n)
            plaintext.append(m)
        print("Success!")
        return "".join([chr(int(k)) for k in plaintext])

    def set_key(self, g, n, lcm, myu):
        self.g, self.n, self.lcm, self.myu = g, n, lcm, myu        

# pal = Paillier()
# cipher = pal.encrypt("aku adalah macan")
# print(cipher)
# plain = pal.decrypt(cipher)
# print(plain)
# print(pal.myu)

def PaillierMain():
    print("==============")
    print("|  Paillier   |")
    print("==============")

    print("Choose Message Source:")
    print("1. File")
    print("2. Input")
    print("--------------")
    msgSource = int(input("Input Message Source Number: "))
    if(msgSource == 1):
        msgPath = str(input("Input Filename: "))
        f = open(msgPath, "r")
        message = f.read()
        message = str(message)
        f.close()
    else:
        message = str(input("Input Message: "))

    print("--------------")
    print("Choose Action:")
    print("1. Encrypt")
    print("2. Decrypt")
    print("--------------")
    action = int(input("Input Action Number: "))
    print("--------------")

    if(action == 1):
        pal = Paillier()
        pal.generate_keys()
        print(pal.encrypt(message))
    else:
        print("Choose Key Source:")
        print("1. From Generated Key")
        print("2. Input")
        print("--------------")
        pal = Paillier()
        keySource = int(input("Input Key Source Number: "))
        print("--------------")

        if(keySource == 1):
            f = open("publicKey.pub", "r")
            key = f.read()
            g,n = key.replace(" ","").split(",")
            g,n = int(g), int(n)
            f.close()
            f = open("privateKey.pri", "r")
            key = f.read()
            lcm,myu = key.replace(" ","").split(",")
            lcm,myu = int(lcm), int(myu)
            f.close()
            pal.set_key(g,n,lcm,myu)
        else:
            g = int(input("Input g Value: "))
            n = int(input("Input n Value: "))
            lcm = int(input("Input lambda Value: "))
            myu = int(input("Input myu Value: "))
            print("--------------")
        print(pal.decrypt(message))
