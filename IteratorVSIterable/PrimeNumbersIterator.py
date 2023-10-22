from PrimeNumbers import PrimeNumbers

class PrimeNumbersIterator(PrimeNumbers):

    def __init__(self, start, end):
        super().__init__(start,end)
        self.index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        numbers = self.getListPrimeNumbers()
        if (self.index < len(numbers)):
            self.index += 1
            return numbers[self.index - 1]
        else:
            raise StopIteration

def main():
    numbers = PrimeNumbersIterator(100,1000)
    
    for _ in range(0,100):
        print(next(numbers))

    for i in numbers:
        print(i)


if (__name__ == "__main__"):
    main()