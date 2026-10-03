"""
1. Create a list of 5 cities. Then:
Add a new city at the end
Insert one at the 2nd position
Remove the last city and print it

2. Create a list of numbers: [3, 1, 4, 1, 5, 9]. Then:
Count how many times 1 appears
Sort the list
Reverse the list

3. Ask the user to enter 3 favorite foods (one by one),
store them in a list, and print the final list.

4. Create a list of 4 student names and:
Print the list in reverse (using slicing)
Check if "John" is in the list

5. Challenge:
Create a list of even numbers from 2 to 20 using list repetition or a loop
(if already covered).
Store multiple student records in a nested list (e.g., ["Alice", 90])
"""

# 1.
cities = ["Jamshedpur", "Lucknow", "Ayodhya", "Gwalior", "Shillong"]
cities.append("Pune")
cities.insert(1, "Bikaner")
print(cities.pop())

# 2.
l1 = [3, 1, 4, 1, 5, 9]
print("Number of times 1 appears -> ", l1.count(1))
l1.sort()
print("List after sorting -> ", l1)
l1.reverse()
print("list after reversing -> ", l1)

# 3.
foods = []
for i in range(3):
    food = input("Enter your favorite food: ")
    foods.append(food)
print(foods)

# 4.

students = ["Jayanth", "Saurabh", "Vinay", "Gowtham"]
print(students[::-1])
print("Yes" if "John" in students else "No")

# 5.
even_numbers = []

for i in range(2, 21, 2):
    even_numbers.append(i)

student_records = [["Jayanth", 99], ["Saurabh", 99], ["Vinay", 100], ["Gowtham", 98]]
print(even_numbers)
print(student_records)
