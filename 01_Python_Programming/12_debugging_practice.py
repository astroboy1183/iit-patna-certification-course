"""
1. Write a program that:
Asks the user to enter two numbers
Adds and multiplies them
Prints both results

2. Introduce an error:
Try adding a string and an integer
Fix it using typecasting

3. Create a program that:
Asks for name and age
Prints: Hi <name>, you will be 100 years old in the year <calculated_year>

4. Write a buggy program that crashes, then fix it:

--python code:--
# Bug: input not converted to int
age = input("Enter your age: ")
years_left = 100 - age
print("Years left to turn 100:", years_left)
--python code:--
"""

from datetime import date

# 1.
num1 = int(input("Enter first number: "))
num2 = int(input("Enter the second number: "))

sum_result = num1 + num2
multiplication = num1 * num2

print(f"The sum of {num1} and {num2} is {sum_result}")
print(f"The multiplication of {num1} and {num2} is {multiplication}")

# 2.
num1 = int(input("Enter first number: "))
num2 = int(input("Enter the second number: "))

sum_result = num1 + num2
multiplication = num1 * num2

print(f"The sum of {num1} and {num2} is {sum_result}")
print(f"The multiplication of {num1} and {num2} is {multiplication}")

# 3.
name = input("Enter your name: ")
age = int(input("Enter your age: "))
curr_year = date.today().year
print(f"Hi {name}, You will be 100 years old in the year {curr_year + 100 - age}")

# 4.
name = input("Enter your name: ")
age = int(input("Enter your age: "))
years_left = 100 - age
print("Years left to turn 100:", years_left)
