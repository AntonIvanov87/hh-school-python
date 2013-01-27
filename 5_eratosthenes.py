#!/usr/bin/python

def eratosthenes(max):

	numbers = range(2, max)

	def filterPrimes(numbers):

		return numbers if len(numbers) == 1 else [numbers[0]] + filterPrimes(filter(lambda i: i%numbers[0] != 0, numbers[1:]))

	return filterPrimes(numbers)


if __name__ == '__main__':

	primes = eratosthenes(20)
	assert primes[0] == 2
	assert primes[7] == 19