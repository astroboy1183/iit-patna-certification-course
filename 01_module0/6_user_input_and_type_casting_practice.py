"""
1. Ask the user for:
Their name
Their birth year

Then print: Hello <name>, you are <age> years old!


2. Ask the user for two numbers and print:
Their sum
Their difference
Their product

3. Ask the user to enter a float number and cast it to integer. Print both values.

4. Ask the user to enter two words and print them in reverse order, separated by a comma.
Example:

Input 1: Hello
Input 2: World
Output: World, Hello

5. Challenge: Ask for a number, multiply it by 5, then convert the result to a string and print:
"Your number multiplied by 5 is: <result>"

"""

from datetime import date

name = input("Enter your name: ")
year = int(input("Enter your birth year: "))
current_year = date.today().year

age = current_year - year

print(f"Hello {name}, you are {age} years old!")


num1 = int(input("Enter a number: "))
num2 = int(input("Enter a number: "))

sum1 = num1 + num2
difference = num1 - num2
product = num1 * num2

print(f"Sum is: {sum1}")
print(f"Difference is: {difference}")
print(f"Product is: {product}")

float_input = float(input("Enter a float input:"))

integer_value = int(float_input)
print(f"Integer value of {float_input} is {integer_value}")

word1 = input("Enter a word: ")
word2 = input("Enter a word: ")

print(f"{word2}, {word1}")

number = int(input("Enter a number: "))
result = number * 5
# result1 = str(result)
print("Your number multiplied by 5 is:", str(result))
