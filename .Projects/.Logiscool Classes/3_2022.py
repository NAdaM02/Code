# Input error
"""try:
    value = int(input('Enter an integer:\n'))
    print(1/value)
except:
    print('Unknown error.')"""

# Exceptions : [ZeroDivisionError, ValueError, TypeError, AttributeError, SyntaxError]
"""try:
    value = int(input('Enter an integer:\n'))
    print(1/value)
except ValueError:
    print('Cannot convert to an integer.')
except ZeroDivisionError:
    print('Cannot divide by zero.')
except:
    print('An unknown error occurred.')"""

"""try:
    f = open('testfile.txt')
    try:
        f.write('Test text')
    except:
        print("Couldn't write to file")
    finally:
        f.close()
except:
    print("Couldn't open file.")"""

# Hibakezelés
# Input error
# value = int(input("Enter an integer:\n"))
# print(value/2)
#
# Hiba eltávolítása
# value = input("Enter an integer:\n")
# if value.isdecimal():
#     value = int(value)
#     print(value/2)
# else:
#     print("Cannot convert to integer")

# Exception kezelés (ZeroDivisionError, ValueError, TypeError, AttributeError, SyntaxError)
# try:
#     value = int(input("Enter an integer:\n"))
#     print(1/value)
# except ValueError:
#     print("Cannot convert to integer")
# except ZeroDivisionError:
#     print("Cannot divide by zero")
# except:
#     print("Unknown error")

# # Szintaxis hiba futó programban
# value = int(input("Enter an integer:\n"))
# if value > 0:
#     print("Positive")
# elif value < 0:
#     prin("Negative")
# else:
#     print("Zero")

# # Finally
# try:
#     f = open("testfile.txt")
#     try:
#         f.write("Test text")
#     except:
#         print("Couldn't write to file")
#     finally:
#         f.close()
# except:
#     print("Couldn't open file")

# Lista elemek összegzése (+ hány db szám?)
#myList = [4, 8, "paper", 15, "code", 16, " ", 23, 42]
#sum = 0
#nums = 0
#for i in range(len(myList)):
#    try:
#        sum += myList[i]
#    except TypeError:
#        print(f"Can't add {myList[i]} to sum. This value is at index: {i}\n")
#    else:
#        nums += 1
#print(sum)
#print(nums)
