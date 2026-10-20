l1 = ["Jayanth", 100, 3.14, False]
l2 = [46235, 344, 75646, 5, 86, 45, 3]

print(type(l1))
print(l1)
print(l1[0])
print(l1[-1])

l1.append("Hyderabad")
l1.append("India")
l1.insert(0, "Python")
l1.insert(2, "games")

print(l1)

l1.remove(100)
l1.pop()

print(l1)

l1[0] = "JayanthAppalla"
print(l1)

print("Before Sorting -> ", l2)
l2.sort()
print("After Sorting -> ", l2)
l2.reverse()
print("After reversing -> ", l2)

l2.append(l1)
print(l2)
l2.extend(l1)
print(l2)
print(l2[0:3])
print(l2[-3:])

print(l2)

l2.append([1, 2, 3, 4, 5])
l2[-1].append([-2, -3, -4, -5])
print(l2)

print(l2[-1][-1][-1])  # should print -5.

print(l2)
l2.insert(1, "Krishna")
print(l2)

l2.pop(4)
print(l2)
