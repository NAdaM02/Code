from math import gcd
abc = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
# Encryption
def Encrypt(string: str, a: int, b: int) :
    x_s = [abc.index(x) for x in list(string.strip())]
    ciphertext = ""
    for x in x_s :
        e = (a*x + b) % m
        ciphertext += abc[e]
    return ciphertext

# Decryption
def Decrypt(string: str, a: int, b: int):
    truetext = ""
    a_m1 = pow(a, -1, m)
    ciphernums = [abc.index(char) for char in list(string)]
    for y in ciphernums :
        d = (a_m1 * (y - b)) % m
        truetext += abc[d]
    return truetext

e_or_d = 'e' if input('Encrypt[e] / Decrypt[d] ?  >') == 'e' else 'd'
string = input("Input = ")
a = int(input("a="))
b = int(input("b="))
m = len(abc)

if __name__ == "__main__" :
    if gcd(a,m) == 1 :
        if e_or_d == 'e' :
            ciphertext = Encrypt(string, a, b)
            print("Input  >", string)
            print("Result >", ciphertext)
            print("keys  a=",a," b=",b, sep="")
        if e_or_d == 'd' :
            truetext = Decrypt(string, a, b)
            print("Input  >", string)
            print("Result >", truetext)
    else:
        print('The conversion is not possible due to a.\na and m must be coprimes!')
