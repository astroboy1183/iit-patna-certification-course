"""
1. Create a dictionary called employee with the following keys:
name, id, position, salary
Print each key-value pair using a loop

2. Write a program to store marks of 3 subjects in a dictionary. Then:
Add the total and average as new keys
Print the updated dictionary

3. Create a contact book where:
Keys are names
Values are phone numbers
Let user enter a name and fetch phone number using .get() safely

4. Use a loop to count frequency of each character in a given string using dictionary.
Input: "apple"
Output: {'a': 1, 'p': 2, 'l': 1, 'e': 1}

5. Bonus Challenge:
Write a program that stores student IDs as keys and nested dictionaries (with name and score) as values.
Then print all student names who scored above 80.
"""

# 1.
employee = {
    "name": "Jayanth",
    "id": "CIS-003",
    "position": "Data Engineer",
    "salary": 10000000,
}
for key, value in employee.items():
    print(key, ":", value)

# 2.

marks = {"Maths": 99, "Physics": 98, "Chemistry": 97}
n = len(marks.keys())
marks["Total"] = sum(marks.values())
marks["Average"] = marks["Total"] / n
print(f"Updated dictionary is as follows: {marks}")

# 3.

contact_book = {
    "Rahul": 1234567890,
    "Ramesh": 2345678901,
    "Ravi": 3456789012,
    "Raj": 4567890123,
}

name = input("Enter name: ")
print(contact_book.get(name, "Name not found in contact book"))

# 4.

char_count = {}
string = "apple"
for char in string:
    if char in char_count:
        char_count[char] += 1
    else:
        char_count[char] = 1

print(char_count)

# 5.

students = {
    1: {"name": "jayanth", "score": 90},
    2: {"name": "ram", "score": 80},
    3: {"name": "rahul", "score": 70},
    4: {"name": "ramesh", "score": 60},
    5: {"name": "ravi", "score": 50},
    6: {"name": "raj", "score": 40},
}

for key, value in students.items():
    if value["score"] > 80:
        print(value["name"])
