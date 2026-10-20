"""
1. Create a tuple of 5 numbers and print:
First and last element
Middle 3 elements using slicing

2. Write a tuple of fruits. Try:
Counting how many times 'apple' appears
Finding the index of 'banana'

3. Create a student tuple: ("Alex", 23, "B.Tech")
Unpack and print: "Name: Alex | Age: 23 | Course: B.Tech"

4. Ask the user to enter 3 favorite movies (one by one), store them in a tuple, and print the result.

5. Challenge:
You have a tuple of numbers. Without converting it to a list:
Loop through the items
Print only the even numbers

"""

# 1.
nums = (1, 2, 3, 4, 5)
print(f"first element: {nums[0]}")
print(f"Last element: {nums[-1]}")
print(f"Middle 3 elements are : {nums[1:4]}")

# 2.
fruits = ("apple", "kiwi", "orange", "banana")
print(f"apple appears {fruits.count('apple')} times")
print(f"Index of banana is {fruits.index('banana')}")

# 3.
student = ("Alex", 23, "B.Tech")
name, age, course = student

print(f"Name: {name} | Age: {age} | Course: {course}")

# 4.
movies_list = []
for i in range(3):
    movies_list.append(input("Enter your favourite movie: "))

movies = tuple(movies_list)
print(movies)

# 5.
nums = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
for i in nums:
    if i % 2 == 0:
        print(i)
