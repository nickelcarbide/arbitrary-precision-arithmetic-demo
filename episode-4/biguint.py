SHIFT = 30
# Shifting left by x is the same as multiplying by 2**x
BASE = 1 << SHIFT

class BigUInt:
	def __init__(self, digits=[]):
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
		self.digits = []

		if (int_from < 0):
			raise ValueError("BigUInt cannot be negative!")

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

	def compare(self, compared_int):
		a = self.digits
		b = compared_int.digits

		if len(a) < len(b):
			return -1 # Lesser

		if len(a) > len(b):
			return 1 # Greater
		
		for i in range(len(a)-1, -1, -1):
			if a[i] < b[i]:
				return -1 # Lesser
			if a[i] > b[i]:
				return 1 # Greater

		return 0 # Equal

	def subtract(self, subtrahend):
		comparison = self.compare(subtrahend)

		# Restricted to unsigned integers
		if comparison == -1:
			raise ValueError("Cannot perform a subtraction that would have a negative result!")
		# If the two BigUInts are equal, the result is zero
		if comparison == 0:
			return BigUInt()

		a = self.digits
		b = subtrahend.digits

		# Simple case for single digit numbers
		if (len(a) == 1) and (len(b) == 1):
			return BigUInt([a[0] - b[0]])

		# Multiple digit numbers
		final_digits = []
		borrow = 0

		# Begin iterating through the digits
		for i in range(len(a)):
			# If there are no digits remaining in the digit of the second number, it is ignored 
			# in the final result. In this case, the algorithm then moves on to the next digit.
			if i >= len(b):
				final_digits.append(a[i] - borrow)
				borrow = 0
				continue

			# If the first number's digit is greater than the second number's digit, with the borrow,
			# there is no need to borrow again, so the difference of these is simply added as a digit.
			if a[i] >= b[i] + borrow:
				final_digits.append(a[i] - b[i] - borrow)
				borrow = 0

			# Otherwise, we do need to borrow, in which case the digit added is the difference 
			# of the two digits added to the base, with any previous borrows subtracted.
			else:
				final_digits.append(BASE + a[i] - b[i] - borrow)
				borrow = 1

		return BigUInt(final_digits)

	def long_multiply(self, multiplier):
		a = self.digits
		b = multiplier.digits

		# Initialize the set of product digits with zeros
		product_digits = [0] * (len(a) + len(b))
		# Iterate through the first number's digits
		for i, digit_a in enumerate(a):
			# Reset the carry
			carry = 0
			# Iterate through the second number's digits
			for j, digit_b in enumerate(b):
				# Add the product of the digits and the carry to the final product
				product_digits[i+j] += carry + digit_a * digit_b
				# Calculate the carry
				carry = product_digits[i+j] // BASE
				# Modulo the digit in the product so that only the last digit remains
				product_digits[i+j] %= BASE
			# The most significant digit comes from the final carry
			product_digits[len(b)+i] = carry

		return BigUInt(product_digits)
