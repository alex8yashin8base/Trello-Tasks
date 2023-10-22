class Numbers:

    __slots__ = ('numbers')

    def __init__(self, numbers):
        self.numbers = numbers

    def __len__(self):
        return len(self.numbers)
    
    def __add__(self,x):
        return Numbers(self.numbers + x.numbers)
    
    def __iter__(self):
        return iter(self.numbers)
    
    def __str__(self):
        return str(self.numbers)
    
    def __getattr__(self, name):
        print (f"attribute '{name}' is not defined")
        return None

    def __getattribute__(self, name):
        print (f"accessing an attribute '{name}'")
        return super().__getattribute__(name)
    
n = Numbers([0]*10)

print (n.numbers)
n.num

k = Numbers([1]*20)
l = n + k

print (len(l))
print (l)