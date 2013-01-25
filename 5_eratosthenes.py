#!/usr/bin/python

def eratosthenes(max):

	numbers = range(2, max)

	def filterPrimes(numbers):

		if len(numbers) == 1:
			return numbers

		prime = numbers[0]
		rest = numbers[1:]
		filteredRest = filter(lambda i: i%prime != 0, rest)

		return [prime] + filterPrimes(filteredRest)


	return filterPrimes(numbers)


if __name__ == '__main__':

	primes = eratosthenes(20)
	print primes