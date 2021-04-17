from biguint import BigUInt

x = BigUInt()
x.from_py_int(5_000_000_000_000)
print("x =", x)
print("x.digits =", x.digits)

y = BigUInt()
y.from_py_int(123_456_789)
print("y =", y)
print("y.digits =", y.digits)

z = x.subtract(y)
print("z = x - y =", z)
print("z.digits =", z.digits)

print()

x = BigUInt()
x.from_py_int(123_456_789_987_654_321_000_000_000)
print("x =", x)
print("x.digits =", x.digits)

y = BigUInt()
y.from_py_int(987_654_321_000_000_000)
print("y =", y)
print("y.digits =", y.digits)

z = x.subtract(y)
print("z = x - y =", z)
print("z.digits =", z.digits)
