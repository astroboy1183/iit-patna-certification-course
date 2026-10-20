"""
1. Given a string "machinelearning", print:
First 5 characters
Last 3 characters
The string in reverse

2. Ask the user to enter their full name. Then:
Print it in uppercase
Print only the first name (assume it’s before the first space)
Count how many times the letter 'a' appears

3. Ask the user for a sentence and print each word in a new line using .split().
4. Replace all spaces in a sentence with dashes (-).
5. Challenge: Ask the user to enter a filename and check if it ends with .py — if yes, print "Python file detected", else "Not a Python file".
"""

# 1.
string = "machinelearning"
print(string[0:5])
print(string[-3:])
print(string[::-1])

# 2.
name = input("Enter Your Full Name: ")
print(name.upper())
print(name.split()[0])
print(name.count("a"))

# 3.
sentence = input("Enter a Sentence: ")
for i in range(len(sentence.split())):
    print(sentence.split()[i])

# 4.
sentence = input("Enter a Sentence: ")
print(sentence.replace(" ", "-"))

# 5.
filename = input("Enter a filename: ")
if filename.endswith(".py"):
    print("Python file detected")
else:
    print("Not a Python file")
