BASE = 2**30

class BigUInt:
	def __init__(self, digits=[]):
		for digit in digits:
			if digit >= BASE:
				raise ValueError("digit is too large!")
		self.digits = digits

	def __int__(self):
		total = 0
		for i, digit in enumerate(self.digits):
			total += digit * (BASE ** i)
		return total

	def __str__(self):
		return str(int(self))

x = BigUInt([])
y = BigUInt([57])
z = BigUInt([10000, 1])

print(x)
print(y)
print(z)
