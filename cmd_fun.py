import os
from time import sleep as wait

words = ["Never ", "gonna ", "give ", "you ", "up","!"]
for word in words:
    os.system(f'start "{word}" cmd')
for i in range(3):
    os.system('start cmd')
    wait(10)