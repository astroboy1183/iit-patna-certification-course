"""
1. Take two numbers as input and print:
Their sum, difference, product, division, and remainder.

2. Ask the user for their age and check:
Are they 18 or older? Print True or False.

3. Ask the user to enter their math and science marks (out of 100). If both are greater than 40, print “Pass”, else “Fail”.

4. Check the result of:

x = 7
print(x > 5 and x < 10)
print(x > 10 or x < 5)
print(not(x > 5))


5. Challenge: Ask for two numbers and print True if the first number is divisible by the second and greater than it.
"""

# 1.
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

print("Sum: ", num1 + num2)
print("Difference: ", num1 - num2)
print("Product: ", num1 * num2)
print("Division: ", num1 / num2)
print("Remainder: ", num1 % num2)

# 2.
age = int(input("Enter your age: "))
print("Are you 18 or older?", age >= 18)

# 3.
math = int(input("Enter your math marks(Out of 100): "))
science = int(input("Enter your science marks(Out of 100): "))

print("Pass" if math > 40 and science > 40 else "Fail")

# 4.
x = 7
print(x > 5 and x < 10)
print(x > 10 or x < 5)
print(not (x > 5))

# 5.
num3 = int(input("Enter first number: "))
num4 = int(input("Enter second number: "))

print(
    "Is first number divisible by second and greater than it?",
    num3 % num4 == 0 and num3 > num4,
)
