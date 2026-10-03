"""
1. Create a function area_of_circle(radius) that returns the area using π ≈ 3.14 and includes a docstring.

2. Use an f-string to print:
Name: Alice, Age: 25, Score: 89.5%

3. USing an fstring, write a program that takes two numbers from the user and prints:
Sum of <a> and <b> is <sum>

4. Write a function is_even(num) that returns True if number is even. Add a docstring explaining the logic.

5. Challenge: Take name and marks as input and print a report card like(use fstring):
Student Report:
---------------
Name: Rahul
Marks: 86.45%
Grade: B+

"""

# 1.


def area_of_circle(radius):
    """
    Finding area of the circle using the formula. pi = 3.14 here.
    """
    pi = 3.14
    return pi * radius * radius


# 2.
name = "Alice"
age = 25
score = 89.5

print(f"Name: {name}, Age: {age}, Score: {score}%")

# 3.
a = int(input("Enter a number: "))
b = int(input("Enter a number: "))

print(f"Sum of {a} and {b} is {a + b}")

# 4.


def is_even(num):
    """
    check if the number is even by checking if it is divisible by 2.
    """
    return num % 2 == 0


# 5.

name = input("Enter your name: ")
marks = float(input("Enter your marks: "))

if marks >= 90:
    grade = "A"
elif marks >= 80 and marks < 90:
    grade = "B+"
elif marks >= 70 and marks < 80:
    grade = "B"
elif marks >= 60 and marks < 70:
    grade = "C"
elif marks >= 50 and marks < 60:
    grade = "D"
else:
    grade = "F"

print("Student Report:")
print("------------------")
print(f"Name: {name}")
print(f"Marks: {marks}%")
print(f"Grade: {grade}")
