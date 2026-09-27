"""

1. Create variables to store your:

Name
Age
Favorite programming language
Whether you’re a student (True/False)

Print each of them with appropriate labels using f-strings.
----------------------------------------------------------------

2. Predict the output and data types:

x = 10
y = 3.14
z = x + y
print(z)
print(type(z))
----------------------------------------------------------------

3. Create a variable with a value "123" and check if it’s a number or string. Then convert it to an integer and add 10.

4. Try creating invalid variable names like 2name, class, or my-name and note what errors Python gives you.
----------------------------------------------------------------

5. Advanced: Can a variable store multiple data types during execution?

x = 10
print(type(x))

x = "Now I am a string"
print(type(x))
----------------------------------------------------------------

"""

Name = "Jayanth Appalla"
Age = 27
Favorite_Programming_Language = "Python"
Student = True

print(f"Name: {Name}")
print(f"Age: {Age}")
print(f"Language: {Favorite_Programming_Language}")
print(f"Student: {Student}")

x = 10
y = 3.14
z = x + y
print(z)  # answer is 13.14
print(type(z))  # type is float

x = "123"
print(type(x))  # type is string

y = int(x) + 10
print(y)
print(type(y))  # type is int

# class = "python" # SyntaxError: invalid syntax
# my-name = "python" #SyntaxError: cannot assign to expression here. Maybe you meant '==' instead of '='?
# 2name = "python" # SyntaxError: invalid decimal literal

x = 10
print(type(x))  # type here is int

x = "Now I am a string"
print(
    type(x)
)  # x points to the string, so type here is string, since in python variable is just pointing to the object, hence it can refer to multiple types.
