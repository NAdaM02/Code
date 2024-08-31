#OOP Exercise 1
"""class Vehicle:
    def __init__(self, max_speed, mileage):
        self.max_speed = max_speed
        self.mileage = mileage

idua = Vehicle(260, 15)
print(idua.max_speed, idua.mileage)"""

#OOP Exercise 2
"""class Vehicle:
    pass"""

#OOP Exercise 3
"""class Vehicle:
    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage

class Bus(Vehicle):
    pass

icarus = Bus("icarus", 160, 11)
print("Name: " + icarus.name + "  |  Max speed: " + str(icarus.max_speed) + "  |  Mileage: " + str(icarus.mileage))"""

#OOP Exercise 4
"""class Vehicle:
    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage

    def seating_capacity(self, capacity):
        return f"The seating capacity of a {self.name} is {capacity} passengers"

class Bus(Vehicle):
    def seating_capacity(self, capacity=50):
        return super().seating_capacity(capacity=50)

icarus = Bus("icarus", 160, 11)
print(icarus.seating_capacity())"""

#OOP Exercise 5
"""class Vehicle:

    color = "white"

    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage

class Bus(Vehicle):
    pass

class Car(Vehicle):
    pass

icarus = Bus("icarus", 160, 11)
idua = Vehicle("idua", 260, 15)
print("Color: " + icarus.color + "  |  Name: " + icarus.name + "  |  Max speed: " + str(icarus.max_speed) + "  |  Mileage: " + str(icarus.mileage))
print("Color: " + idua.color + "  |  Name: " + idua.name + "  |  Max speed: " + str(idua.max_speed) + "  |  Mileage: " + str(idua.mileage))"""

#OOP Exercise 6
"""class Vehicle:
    def __init__(self, name, mileage, capacity):
        self.name = name
        self.mileage = mileage
        self.capacity = capacity

    def fare(self):
        return self.capacity * 100

class Bus(Vehicle):
    def fare(self):
        amount = super().fare()
        amount += amount * 10 / 100
        return amount

icarus = Bus("icarus", 160, 11)
print("Total Bus fare is:", icarus.fare())"""

#OOP Exercise 7
"""class Vehicle:
    def __init__(self, name, mileage, capacity):
        self.name = name
        self.mileage = mileage
        self.capacity = capacity

class Bus(Vehicle):
    pass

icarus = Bus("icarus", 160, 11)
print(type(icarus))
"""

#OOP Exercise 8
"""class Vehicle:
    def __init__(self, name, mileage, capacity):
        self.name = name
        self.mileage = mileage
        self.capacity = capacity

class Bus(Vehicle):
    pass

icarus = Bus("icarus", 160, 11)
print(isinstance(icarus, Vehicle))"""
