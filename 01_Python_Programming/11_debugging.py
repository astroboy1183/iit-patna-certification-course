# print, escape, comments
print("Welcome to my python program. \nLet's get to know more about you.")

# variable, datatypes and typecasting
name = input("Please enter your name here -> ")
age = int(input("Please enter your age here -> "))

print(f"\nHello {name}, nice to meet you. You're {age} years old.")

# arithmetic, logical and comparison operators

num1 = float(input("Please enter first number here -> "))
num2 = float(input("Please enter first number here -> "))

sum_result = num1 + num2
product = num1 * num2
division = num1 // num2

# comparison operator

is_equal = num1 == num2
is_greater = num1 > num2

# logical operator

both_positive = num1 > 0 and num2 > 0

print(f"The sum of {num1} and {num2} is {sum_result}")
print(f"The product of {num1} and {num2} is {product}")
print(f"The division of {num1} and {num2} is {division}")
print(f"Is {num1} equal to {num2}? -> {is_equal}")
print(f"Is {num1} greater than {num2}? -> {is_greater}")
print(f"Are both {num1} and {num2} positive? -> {both_positive}")

# strings: slicing, indexing, methods

print("Hello, This is your name. ")
print(f"Your name in upper case is: {name.upper()}.")
print(f"Your name in lower case is: {name.lower()}.")
print("Your name in reverse order is: ", name[::-1])
print(f"The first 3 characters of your name are: {name[0:2]}")
