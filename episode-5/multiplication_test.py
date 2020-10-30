from biguint import BigUInt

x = BigUInt()
x.from_py_int(12_341_234)
y = BigUInt()
y.from_py_int(2_000_000_000)
z = x.karatsuba_multiply(y)

print("x =", x)
print("y =", y)
print("x * y =", z)
print()

x = BigUInt()
x.from_py_int(1234567890000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
y = BigUInt()
y.from_py_int(1000000000000000000000000000000000000000000000000000000000)
z = x.karatsuba_multiply(y)

print("x =", x)
print("y =", y)
print("x * y =", z)
print()

x = BigUInt()
x.from_py_int(31415926535897932384626433832795028841971693993751058209749445923078164062862)
y = BigUInt()
y.from_py_int(99999999999999999999999999999999999999999999999999999999999999999999999999999)
z = x.karatsuba_multiply(y)

print("x =", x)
print("y =", y)
print("x * y =", z)
