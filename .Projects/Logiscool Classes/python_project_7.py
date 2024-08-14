class Triangle:
    def perimiter(self, a, b, c):
        return a+b+c
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
t1 = Triangle(3,4,5)
result = t1.perimiter(t1.a,t1.b,t1.c)
print(result)
