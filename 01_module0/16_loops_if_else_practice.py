"""
1. Write a program to check if a number is even or odd using if-else.
2. Loop through numbers 1 to 10 and print only even numbers using continue.
3. Ask the user to guess a number between 1–5.
Keep asking until the guess is correct (use while and break).
4. Use a for loop to calculate the sum of all numbers between 1 and 100.
5. Write a program to count how many vowels are in a given string using a for loop.

6. BONUS: Create a simple login system:
Username: "admin"
Password: "1234"
Allow user 3 attempts. If correct, print "Login successful", else "Account locked".
"""

from getpass import getpass

# 1.

num = int(input("Enter a number: "))
if num % 2 == 0:
    print("Even")
else:
    print("Odd")

# 2.

for i in range(1, 11):
    if i % 2 != 0:
        continue
    else:
        print(i)

# 3.

actual = 3
while True:
    guess = int(input("Guess a number: "))
    if actual == guess:
        break

# 4.

sum1 = 0
for i in range(2, 100):
    sum1 += i
print("Sum: ", sum1)

# 5.

vowels = ["a", "e", "i", "o", "u"]
string = input("Enter a string: ")

alphabets = list(string.lower())
count = 0
for alphabet in alphabets:
    if alphabet in vowels:
        count += 1

print("Number of vowels: ", count)

# 6.

num_attempts = 3

while num_attempts >= 1:
    user_name = input("Enter your username: ")
    password = getpass("Enter your password: ")
    if user_name == "admin" and password == "1234":
        print("Login successful!")
        break
    else:
        num_attempts -= 1
        print("Try again.")
if num_attempts == 0:
    print("Account locked")
