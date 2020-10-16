from biguint import BigUInt

x = BigUInt()
x.from_py_int(25)
y = BigUInt()
y.from_py_int(25)
z = x.long_multiply(y)

print("x =", x)
print("y =", y)
print("x * y =", z)
print()

x = BigUInt()
x.from_py_int(12_341_234)
y = BigUInt()
y.from_py_int(2_000_000_000)
z = x.long_multiply(y)

print("x =", x)
print("y =", y)
print("x * y =", z)
print()

x = BigUInt()
x.from_py_int(3_141_592)
y = BigUInt()
y.from_py_int(61_092_399_581_409_512)
z = x.long_multiply(y)

print("x =", x)
print("y =", y)
print("x * y =", z)
