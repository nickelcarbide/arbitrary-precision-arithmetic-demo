SHIFT = 30
# Shifting left by x is the same as multiplying by 2**x
BASE = 1 << SHIFT

class BigUInt:
	def __init__(self, digits):
		for digit in digits:
			if digit >= BASE:
				raise ValueError("digit is too large!")
		self.digits = digits

	def __int__(self):
		total = 0
		for i, digit in enumerate(self.digits):
			total += digit << (SHIFT * i)
		return total

	def __str__(self):
		return str(int(self))

	def from_py_int(self, int_from):
		if (int_from < 0):
			raise ValueError("BigUInt digit cannot be negative!")

		next_digit = int_from

		# This is repeated until there are no more digits left
		while next_digit > 0:
			# The next digit is set to the remainder from the base
			self.digits.append(next_digit % BASE)
			
			# The next digit is obtained by dividing by the base
			next_digit >>= SHIFT

	def add(self, added_int):
		# Assume the first int has more digits
		greater_digits = self.digits
		lesser_digits = added_int.digits
		# If this assumption is wrong, correct it
		if len(self.digits) < len(added_int.digits):
			greater_digits, lesser_digits = added_int.digits, self.digits

		# Initialization
		final_digits = []
		sum_digit = 0
		carry = 0
		
		# Begin iterating through the digits
		for i in range(len(greater_digits)):
			# If there are no longer any digits from the lesser digit number, it is ignored in the sum
			if i < len(lesser_digits):
				sum_digit = greater_digits[i] + lesser_digits[i] + carry
			else:
				sum_digit = greater_digits[i] + carry

			# If the sum is larger than the base, add the remainder from the base as a digit and set the carry to 1
			if sum_digit >= BASE:
				final_digits.append(sum_digit % BASE)
				carry = 1
			# Otherwise, add the sum as a digit and set the carry to 0
			else:
				final_digits.append(sum_digit)
				carry = 0

		# If there is still a carry left over at the end, add this as a digit
		if carry > 0:
			final_digits.append(carry)

		return BigUInt(final_digits)

x = BigUInt([])
x.from_py_int(10_000_000_000_000_000_000)
print("x =", x)
print(x.digits)

y = BigUInt([])
y.from_py_int(3_000_000_000_000_000_000)
print("y =", y)
print(y.digits)

z = x.add(y)
print("z =", z)
print(z.digits)
