from PrimeNumbers import PrimeNumbers

class PrimeNumbersIterable(PrimeNumbers):

    def __iter__(self):
        return iter(self.getListPrimeNumbers())

def main():
    numbers = PrimeNumbersIterable(100,1000)
    it = iter(numbers)

    for _ in range(0,100):
        print(next(it))

    for i in it:
        print(i)

if (__name__ == "__main__"):
    main()