# basics of if-else

"""
Write a program that will ask the user for climate/temperature of their location.

1. Check if temperature is greater than or equals to 30.
    If yes, then print a message notifying the user about hot climate.
2. Check if the temperature is lesser than or equals to 15.
    If yes, then print a message notifying the user about cold climate.

3. Otherwise, print "Have a nice day."
"""

print("Hello, Welcome to my first if-else program.")
temp = int(input("What is the temperature at your location? -> "))

if temp >= 30:
    print("It seems hot there, you're suggested to stay inside the house.")
elif temp <= 15:
    print("It seems really cold there, enjoy the sun.")
else:
    print("It seems fine there. Have a nice day.")

# basics of loops
fruits = ["apple", "banana", "kiwi", "mango"]

for i in fruits:
    print(i.capitalize())

for i in fruits:
    print(f"We are here -> {i}")

fruits = ["apple", "banana", "kiwi", "mango", 3]

for i in fruits:
    if type(i) == int:
        print(f"Number: {i}")
    else:
        print(f"String: {i}")
