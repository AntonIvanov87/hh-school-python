#!/usr/bin/python

def primes(max):

	def sieve(numbers, non_primes, max):

		# this if is legal - it has return and can be treated as guard in functional lanuages
		# we can rewrite it with if conditional expression
		# but the code will become not readable
		if len(numbers) == 0:
			return []

		elif numbers[0] in non_primes:

			return sieve(numbers[1:], non_primes - set(numbers[0:1]), max)

		else:

			# this = is legal - it is just a synonym to make next expression more readable
			new_non_primes = non_primes.union(set(range(numbers[0]*2, max, numbers[0])))
			# we can do better:
			# now if we see 2 we add 4, 6, 8... into the new_non_primes
			# we can add only 4 instead and remember that 4 was added because of prime 2
			# later, when we see 4, we can substitue it with 6 instead, etc.
			# thus on every recursion we can maintain only minimum number of non_primes required
			# but it will be pretty hard to implement this without statements
			# thus I decided to leave this version

			return numbers[0:1] + sieve(numbers[1:], new_non_primes, max)

	return sieve(range(2, max), set(), max)


if __name__ == '__main__':

	primes_list = primes(20)
	assert primes_list[0] == 2
	assert primes_list[7] == 19