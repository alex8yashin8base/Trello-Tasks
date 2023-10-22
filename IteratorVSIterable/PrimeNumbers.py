class PrimeNumbers:

    def __init__(self, start, end):
        if (start < 0):
            self.start = 0
        else:
            self.start = start

        if (end < 0):
            self.end = 0
        elif (end < start):
            self.end = start
        else:
            self.end = end

    def primality(self, number):
        if number <= 1:
            return False
        if number <= 3:
            return True
    
        if number % 2 == 0 or number % 3 == 0:
            return False
    
        i = 5
        while i * i <= number:
            if number % i == 0 or number % (i + 2) == 0:
                return False
            i += 6
    
        return True
    
    def getListPrimeNumbers(self):
        result = []
        for i in range(self.start, self.end + 1):
            if (self.primality(i)):
                result.append(i)
        return result