from biguint import BigUInt

x = BigUInt()
x.from_py_int(5_000_000_000_000)
print("x =", x)
print("x.digits =", x.digits)

y = BigUInt()
y.from_py_int(123_456_789)
print("y =", y)
print("y.digits =", y.digits)

x.compare(y)
print("comparison =", x.compare(y))

print()

x.from_py_int(555_555)
print("x =", x)
print("x.digits =", x.digits)

y.from_py_int(8_132_129_309_329_813_280_982)
print("y =", y)
print("y.digits =", y.digits)

x.compare(y)
print("comparison =", x.compare(y))

print()

x.from_py_int(2_000_000_000)
print("x =", x)
print("x.digits =", x.digits)

y.from_py_int(6_000_000_000)
print("y =", y)
print("y.digits =", y.digits)

x.compare(y)
print("comparison =", x.compare(y))

print()

x.from_py_int(9_999_999_999_999)
print("x =", x)
print("y.digits =", x.digits)

y.from_py_int(9_999_999_999_999)
print("y =", y)
print("y.digits =", y.digits)

x.compare(y)
print("comparison =", x.compare(y))
