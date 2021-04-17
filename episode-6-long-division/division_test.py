from biguint import BigUInt

x = BigUInt()
x.from_py_int(4_830_982_092_138_231)
y = BigUInt()
y.from_py_int(1_000_000_000_000_000_000_000_000)
z = x.divide(y)

print("x =", x)
print("y =", y)
print("x / y =", z[0])
print("x % y =", z[1])
print()

x = BigUInt()
x.from_py_int(79_000_000_000_000_000_000_000_000_000)
y = BigUInt()
y.from_py_int(79)
z = x.divide(y)

print("x =", x)
print("y =", y)
print("x / y =", z[0])
print("x % y =", z[1])
print()

x = BigUInt()
x.from_py_int(79_000_000_000_000_000_000_000_000_000)
y = BigUInt()
y.from_py_int(1_000_000_000_000_000_000_000_000)
z = x.divide(y)

print("x =", x)
print("y =", y)
print("x / y =", z[0])
print("x % y =", z[1])
print()

x = BigUInt()
x.from_py_int(1_000_000_000_000_000_000_000_000)
y = BigUInt()
y.from_py_int(2_000_000_000_000_000_000_000_000)
z = x.divide(y)

print("x =", x)
print("y =", y)
print("x / y =", z[0])
print("x % y =", z[1])
print()
