SHIFT = 30
# Shifting left by x is the same as multiplying by 2**x
BASE = 1 << SHIFT

class BigUInt:
	def __init__(self, digits=[]):
		for digit in digits:
			if digit >= BASE:
				raise ValueError("digit is too large!")
		self.digits = digits
		self.normalize()

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

		answer = BigUInt(final_digits)
		answer.normalize()
		return answer

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

		answer = BigUInt(final_digits)
		answer.normalize()
		return answer

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

	def karatsuba_multiply(self, multiplier):
		# Use asymptotically slower long multiplication for small enough numbers
		if len(self.digits) < 4 or len(multiplier.digits) < 4:
			return self.long_multiply(multiplier)

		# Split the digits into halves
		split_point = min(len(self.digits), len(multiplier.digits)) // 2
		a = BigUInt(self.digits[split_point:])
		b = BigUInt(self.digits[:split_point])
		c = BigUInt(multiplier.digits[split_point:])
		d = BigUInt(multiplier.digits[:split_point])

		# Calculate the variables for multiplication
		f = a.karatsuba_multiply(c)
		g = b.karatsuba_multiply(d)
		h = a.add(b).karatsuba_multiply(c.add(d))
		k = h.subtract(g).subtract(f)

		# Shift k and f to the correct significance
		k_shifted = BigUInt(split_point * [0] + k.digits)
		f_shifted = BigUInt(2 * split_point * [0] + f.digits)

		# Add the digits together for the final product
		answer = g.add(k_shifted).add(f_shifted)
		answer.normalize()
		return answer

	def normalize(self):
		# This method strips zeros from the beginning of a number
		# As having leading zeros causes issues with comparing the amount of digits in numbers
		
		# Iterate backwards through the digits
		i = len(self.digits)-1
		while i >= 0:
			# If a non-zero digit is found, stop iterating
			if self.digits[i] != 0:
				break
			i -= 1
		# Set the number to the new digits without the leading zeros
		self.digits = self.digits[0:i+1]

	def divide(self, divisor):
		# This method returns a tuple of both the quotient and remainder

		a = self.digits
		b = divisor.digits

		# Initialize digits
		
		quotient_digits = []
		remainder_digits = []

		im_dividend = BigUInt() # Intermediate dividend

		if len(a) < len(b):
			# If the amount of digits in first number is less than second number, 
			# the quotient is 0 and the remainder is the same as the first number
			remainder_digits = a
		else:
			# Otherwise, initialize the intermediate remainder, then begin iterating
			if len(b) >= 2:
				remainder_digits = a[-len(b)+1:]

			# The amount of iterations is equal to the difference of lengths of the two numbers.
			for i in range(0, len(a)-len(b)+1):
				# Add the next digit of the dividend to the i.m. dividend
				im_dividend = BigUInt([0] + remainder_digits).add( BigUInt([ a[-i-len(b)] ]) )

				# Find the next digit of the quotient using a binary search.
				# The next digit of the quotient is the greatest multiple of the divisor less 
				# than the i.m. dividend.
				q_next = None
				min_q = 0
				max_q = BASE - 1
				while min_q <= max_q:
					# The guess for the next quotient digit is in the middle of the last 2
					q_next = (min_q + max_q) >> 1

					# Compare the i.m. dividend and the guess for the greatest multiple of 
					# the divisor less than the i.m. dividend.
					comparison = im_dividend.compare(
						divisor.karatsuba_multiply( BigUInt([ q_next ]) )
					)

					if comparison == 1:
						min_q = q_next + 1
					elif comparison == -1:
						max_q = q_next - 1
					else:
						break

				# This accounts for divisions with a remainder
				q_next = (min_q + max_q) >> 1

				# Calculate the remainder by subtracting the greatest multiple of the divisor 
				# less than the i.m. dividend from the i.m. dividend.
				remainder_digits = im_dividend.subtract(
					divisor.karatsuba_multiply( BigUInt([ q_next ]) )
				).digits

				quotient_digits = [q_next] + quotient_digits

		answer = (BigUInt(quotient_digits), BigUInt(remainder_digits))
		answer[0].normalize()
		answer[1].normalize()
		return answer
