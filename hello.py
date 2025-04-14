# write a function call add that add two positive integers
def add(a: int, b: int) -> int: 
    """
    Add two positive integers.
    
    :param a: First positive integer
    :param b: Second positive integer
    :return: Sum of a and b
    """
    return a + b

def multiply(a: int, b: int) -> int:
    """
    Multiply two positive integers.
    
    :param a: First positive integer
    :param b: Second positive integer
    :return: Product of a and b
    """
    return a * b

def subtract(a: int, b: int) -> int:
    """
    Subtract two positive integers.
    
    :param a: First positive integer
    :param b: Second positive integer
    :return: Difference of a and b
    """
    return a - b
def divide(a: int, b: int) -> float:
    """
    Divide two positive integers.   
    
    :param a: First positive integer
    :param b: Second positive integer
    :return: Quotient of a and b
    """

def main():
    print("Hello from api-versioning-github-copilot!")
    print("The sum of 2 and 3 is:", add(2, 3))
    print("The product of 2 and 3 is:", multiply(2, 3))
    print("The difference of 2 and 3 is:", subtract(2, 3))
    

if __name__ == "__main__":
    main()
