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
			return numbers[0:1] + sieve(numbers[1:], new_non_primes, max)

	return sieve(range(2, max), set(), max)


if __name__ == '__main__':

	primes_list = primes(20)
	assert primes_list[0] == 2
	assert primes_list[7] == 19