from typing import Any


class FOO:
    def __init__(self):
        self.bar = 10
        
    def __getattribute__(self, x):
        print ("eee")
        return self.x

f = FOO()
f.bar = 100
print (f.bar)