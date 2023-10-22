import re

PATH = "Decorator/log.txt"
EXIT_PHRASE = "exit"

def audit_log(path):

    def decorator(func):
        def wrapper(*args, **kwargs):

            result = func(*args, **kwargs)
            event = f"The '{func.__name__}' operation was performed with '{args}' arguments, the result is '{result}'\n"

            file = open(path, "a")
            file.write(event)
            file.close()

            return result
        return wrapper
    
    return decorator

@audit_log(PATH)
def calculate(expression):
    return eval(expression)

def main():
    while True:
        expression = input()
        if expression == EXIT_PHRASE:
            break
        else:
            print(calculate(expression))

if (__name__ == "__main__"):
    main()