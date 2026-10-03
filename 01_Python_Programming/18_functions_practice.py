"""
1. Create a function greet_user(name) that prints:
"Hello, <name>. Welcome to Python!"

2. Write a function add(a, b) that returns the sum. Add a default value of b=0.
3. Create a function max_of_all(*args) that prints the maximum number from a list of numbers.
4. Create a function print_student(**kwargs) that accepts arbitrary student details and prints them.

5. Challenge: Write a function calculate(operation, *args) that performs the operation (like 'add', 'multiply') on the numbers passed.
calculate("add", 1, 2, 3)       # 6
calculate("multiply", 2, 3, 4)  # 24
"""


# 1.
def greet_user(name):
    print(f"Hello, {name}. Welcome to Python!")


# 2.
def add(a, b=0):
    return a + b


# 3.
def max_of_all(*args):
    print("Maximum number is:", max(args))


# 4.
def print_student(**kwargs):
    for i in kwargs.items():
        print("Key:", i[0], "Value:", i[1])


# 5.
def calculate(operation, *args):

    if operation == "add":
        sum1 = 0
        for i in args:
            sum1 += i
        return sum1
    elif operation == "subtract":
        diff = args[0]
        for i in range(1, len(args)):
            diff -= args[i]
        return diff
    elif operation == "multiply":
        product = 1
        for i in args:
            product *= i
        return product
    elif operation == "divide":
        div = args[0]
        for i in range(1, len(args)):
            div /= args[i]
        return div
    else:
        return "Invalid operation"


greet_user("Jayanth")
print(add(2, 3))
print(add(5))
max_of_all(4, 9, 2)
print_student(name="Jayanth", age=27, course="GenAI")
print(calculate("add", 1, 2, 3))
print(calculate("multiply", 2, 3, 4))
