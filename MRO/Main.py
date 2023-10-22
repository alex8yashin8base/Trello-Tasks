class O: 
    def foo(self):
        print("fooO")

class A(O):
    def foo(self):
        print("fooA")

class B(O):
    def foo(self):
        print("fooB")

class C(O):
    def foo(self):
        print("fooC")

class D(O):
    def foo(self):
        print("fooD")

class E(O):
    def foo(self):
        print("fooE")

class K1(A, B, C):
    def fooK(self):
        print("fooK1")

class K2(B, D):
    def fooK(self):
        print("fooK2")
    def foo2(self):
        print("fooK2")

class K3(C, D, E):
    def fooK(self):
        print("fooK3")
    def foo2(self):
        print("fooK3")

class Z(K1, K2, K3):
    def fooZ(self):
        print("fooZ")

def print_mro(T):
    print(*[c.__name__ for c in T.mro()], sep=' -> ')

print_mro(Z)

z = Z()
z.foo()
z.fooK()
z.foo2()