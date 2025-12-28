s =set()
s.add(1)
s.add(3)
s.add(2)
print(s)
s.add(1)
print(s)
print(f"The sets has {len(s)} elements")
for i in range(6):
    print(i)
for i in s:
    print(s[i]) #does not work on sets   