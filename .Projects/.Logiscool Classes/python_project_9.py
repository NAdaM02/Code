date = 2022
class Programmer:
    def __init__(self,name,born_in):
        self.name = name
        self.born_in = born_in
    def get_age(self):
        return date-self.born_in
p1 = Programmer("Józsi", 1967)
print(f"{p1.name} {p1.get_age()} éves.")

class Temperatures:
    def __init__(self, degrees):
        self.degrees = degrees
    def get_in_fahrenheit(self):
        return (self.degrees * 9/5) + 32
c1 = Temperatures(12)
"""print(c1.get_in_fahrenheit())"""
