import math
import random

class Elgamal:
    def __init__(self, text, decrypt=None, p=None, x=None):
        self.text = text.lower().replace(" ","")
        if(decrypt==True):
            self.p = p
            self.x = x
            self.decryptTuples = text.replace("(","").replace(")","").split(", ")
    
    def generate_keys(self):
        foundEven = False

        while(foundEven == False):
            fo = open('primes.txt', 'r')
            lines = fo.read().splitlines()
            fo.close()

            randPrime = random.randint(100, 300)
            p = int(lines[randPrime])
            g = random.randint(0,p-1)
            x = random.randint(1,p-2)
            
            if(len(str(p)) % 2 == 0):
                foundEven = True

        y = (g**x) % p

        f_public = open('publicKey.pub', 'w')
        f_public.write(str(y) + ', ' + str(g) + ', ' + str(p))
        f_public.close()

        f_private = open('privateKey.pri', 'w')
        f_private.write(str(x) + ', ' + str(p))
        f_private.close()

        return y,g,p,x
    
    def msgBlocking(self, processedMsg, n):
        msgBlock = []
        blockingProcessing = True
        blockSize = len(str(n))

        while(blockingProcessing):
            if(len(processedMsg) == 0):
                blockingProcessing = False
            else:
                temp = ""
                if(len(processedMsg) < blockSize):
                    for i in range(blockSize - (len(processedMsg) % blockSize)):
                        processedMsg = "0" + processedMsg
                
                for i in range(blockSize):
                        temp += processedMsg[0]
                        processedMsg = processedMsg[1:]

                if((int(temp) > n-1)):
                    processedMsg = temp[-2:] + processedMsg
                    temp = temp[:-2]
                    for i in range(len(str(n)) - len(temp)):
                        temp = "0" + temp
                
                msgBlock.append(temp)
        return msgBlock

    def encrypt(self):
        self.y, self.g, self.p, self.x = self.generate_keys()

        processedMsg = ""
        for letter in self.text:
            alphOrder = str(ord(letter) - 96)
            if(len(alphOrder) < 2):
                alphOrder = "0" + alphOrder
            processedMsg += alphOrder
        
        msgBlock = self.msgBlocking(processedMsg, self.p)

        randK = random.randint(1, self.p-2)
        
        aRes = ""
        bRes = ""
        stringRes = ""
        for blocks in msgBlock:
            blockReady = False
            while(blockReady == False):
                if(blocks[0] == 0):
                    blocks = blocks[1:]
                else:
                    blockReady = True
            
            a = (self.g**randK) % self.p
            b = ((self.y**randK)*int(blocks)) % self.p

            stringRes += "(" + str(a) + "," + str(b) + "), "
        
        stringRes = stringRes[:-2]

        encryptTuple = stringRes

        f_output = open('output.txt', 'w')
        f_output.write(encryptTuple)
        f_output.close()

        return encryptTuple

    def decrypt(self):
        decryptedText = []
        for tuples in self.decryptTuples:
            a,b = tuples.split(",")
            a = int(a)
            b = int(b)
            aPowerX = (a ** (self.p-1-self.x)) % self.p
            blockRes = (b * aPowerX) % self.p
            
            if(len(str(blockRes)) < len(str(self.p))):
                for i in range(len(str(self.p)) - len(str(blockRes))):
                    blockRes = "0" + str(blockRes)

            decryptedText.append(str(blockRes))
        
        processedDecryptedText = ""
        for blocks in decryptedText:
            processedDecryptedText += blocks

        decryptResult = ""
        for i in range(int(len(processedDecryptedText) / 2)):
            temp = ""
            if(processedDecryptedText[0] == "0" and processedDecryptedText[1] == "0"):
                for j in range(2):
                    processedDecryptedText = processedDecryptedText[1:]
            else:
                if(processedDecryptedText[0] != "0"):
                    for j in range(2):
                        temp += processedDecryptedText[0]
                        processedDecryptedText = processedDecryptedText[1:]
                else:
                    temp += processedDecryptedText[1]
                    processedDecryptedText = processedDecryptedText[2:]
                temp = chr(int(temp) + 96)
                decryptResult += temp
        
        return decryptResult

def ElgamalMain():
    print("===============")
    print("|   Elgamal   |")
    print("===============")

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
        print("Encrypting...")
        elgamal = Elgamal(message)
        print(elgamal.encrypt())
    else:
        print("Choose Key Source:")
        print("1. From Generated Key")
        print("2. Input")
        print("--------------")
        keySource = int(input("Input Key Source Number: "))
        print("--------------")

        if(keySource == 1):
            f = open("privateKey.pri", "r")
            key = f.read()
            x1,p1 = key.replace(" ","").split(",")
            x1,p1 = int(x1), int(p1)
            f.close()
        else:
            x1 = int(input("Input x Value: "))
            p1 = int(input("Input p Value: "))
            print("--------------")
        print("Decrypting...")
        elgamal = Elgamal(message, decrypt=True, p=p1, x=x1)
        print(elgamal.decrypt())
