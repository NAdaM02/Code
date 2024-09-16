"""5-ös
Be: Egész szám (>0)
Ki: Prímosztói felsorolva hatvány és szorzat alakban
Be: 11
Ki: 11

Be: 18
Ki: 2*3^2"""

def get_next_prime(number):
    n = number
    while True:
        n += 1
        
        is_prime = True
        for d in range(2, int((n**(1/2)))+1):
            if n%d == 0:
                is_prime = False
                break

        if is_prime:  return n

def count_in_list(c_list, element):
    count = 0
    for list_element in c_list:
        if element == list_element:
            count += 1
    return count


if __name__ == "__main__":
    
    print("This program will output a given number's prime factorization.")
    number = int(input())

    if number <= 0:
        raise Exception("Give a whole number above 0!")

    primes = []

    x = number
    p = 2
    while 1 < x:
        if x % p == 0:
            x //= p
            primes.append(p)
        else:
            p = get_next_prime(p)

    doubles = []
    prime_factorized_string=""
    for prime in primes:
        if not prime in doubles:
            doubles.append(prime)

            prime_count = count_in_list(primes, prime)

            if prime_count != 1:
                factor = f"^{prime_count}"
            else:
                factor = ""

            prime_factorized_string += f"{prime}{factor}*"

    print(prime_factorized_string[:-1])
