# a = 10
# b = 5

# print("Addition: ", a + b)
# print("Subtraction: ", a - b)
# print("Multiplication: ", a * b)
# print("Division: ", a / b)
# print("Modulus: ", a % b)
# print("Floor Division: ", a // b)
# print("Exponent: ", a**b)

# # comparison operators

# x = 20
# y = 10

# print("x > y is", x > y)
# print("x < y is", x < y)
# print("x == y is", x == y)
# print("x != y is", x != y)
# print("x >= y is", x >= y)
# print("x <= y is", x <= y)

x = round(3.14, 0)
y = 3

print("x: ", x)
print("y: ", y)
print("x > y is", x > y)
print("x < y is", x < y)
print("x == y is", x == y)
print("x != y is", x != y)
print("x >= y is", x >= y)
print("x <= y is", x <= y)

age = 20
has_license = True
print("ELigible to drive? ", age >= 18 and has_license)

has_license = False
print("Eligible to drive? ", age >= 18 or has_license)

age = 18
print("Is eligible to drink? ", not age < 21)
