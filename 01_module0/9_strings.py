name = "jayanthapalla@gmail.com"
print(id(name.capitalize()))
print(name)

print(id(name))

print(name[3])
print(name[-1])

print(name[0:4])

print(name[::-1])

print(name[0] + name[1] + name[2] + name[3] + name[4] + name[5] + name[6])

print(name[::])
print(name[::1])
print(name[::2])
print(name[::-1])
print(name[::3])

a = "abc"
b = "def"
c = a + b
print(c)
print(a + " " + b)
print(a * 4)

print("abc" in c)
print("def" in c)
print("ghi" in c)
print("abc" not in c)
print("def" not in c)
print("ghi" not in c)
print(len(a))

newstring = "    JayanthAppalla   "
newstring.lower()
newstring.upper()

print(newstring.lower())
print(newstring.upper())
print(newstring.strip())
print(newstring.rstrip())
print(newstring.lstrip())

my_name = "Jayanth Appalla"
my_name1 = "Jayanth||Appalla"

print(my_name.split())
print(my_name.split("|"))
print(my_name1.split("||"))

print(my_name.strip())
print(my_name.split()[0] + my_name.split()[1])
