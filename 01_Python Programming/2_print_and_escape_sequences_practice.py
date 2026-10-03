"""
1. Add comments to this code to explain what each line does:

---
name = "Alice"
print("Hello", name)
---

2. Use escape sequences to format the following:

---
Output should be:
Name:    John
Age:     30
He said, "I'm learning Python."
---

3. Print this using only one print statement:

---
Apple | Banana | Mango <End>
---

4. (Challenge) Write a multi-line message using \n and \t to format it like:

---
Welcome to Python!
        Learn to code
                Have fun!
---
"""

name = "Alice"  # stores alice in variable name
print("Hello", name)  # prints hello alice

print('Name:\tJohn\nAge:\t30\nHe said, "I\'m learning Python."')

print("Apple", "Banana", "Mango", sep=" | ", end=" <End>")

print("\n")

print("Welcome to Python!\n\tLearn to code\n\t\tHave fun!")
