"""
1. Remove Duplicates from a List
nums = [1, 2, 2, 3, 4, 4, 5]
# Write code to remove duplicates and print sorted result

2. Find Common Items Between Two Lists
list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
# Use sets to print the common elements

3. Set Difference
a = [1, 2, 3, 4, 5]
b = [3, 4, 6]
# Print elements in a but not in b

4. Fast Membership Check
words = ["apple", "banana", "grape", "orange"]
# Convert to set and check if "grape" exists
"""

# 1.
nums = [1, 2, 2, 3, 4, 4, 5]
print(sorted(set(nums)))

# 2.
list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
print(set(list1).intersection(set(list2)))

# 3.
a = [1, 2, 3, 4, 5]
b = [3, 4, 6]

print(set(a) - set(b))

# 4.
words = ["apple", "banana", "grape", "orange"]
print("grape" in set(words))

# l = [1578, 2121212, 3333, 4444]
# print(id(l[-1]))
# l.pop()
# l.append(44444)
# l.append(4444)
# print(id(l[-1]))
