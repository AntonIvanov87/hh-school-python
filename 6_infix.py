#!/usr/bin/python

class InfixOperator:
	"""
	Allows to simulate infix operators.
	"""

	def __init__(self, func):
		"""
		func - function to be called on two arguments.
		"""

		self.func = func


	def __ror__(self, other):

		return InfixOperatorWithLeftArg(self.func, other)


class InfixOperatorWithLeftArg:
	"""
	Service class that supports InfixOperator.
	"""

	# Decided to make separate class to stress that
	# InfixOperator can only __ror__, and does not need leftArg
	# InfixOperatorWithLeftArg can only __or__, and always need leftArg
	# We can make checks and throw exceptions, but in my opinion it is not a better solution
	# Besides our classes are "immutable": they do not change their state inside methods

	def __init__(self, func, leftArg):

		self.func = func
		self.leftArg = leftArg


	def __or__(self, other):

		return self.func(self.leftArg, other)


if __name__ == '__main__':

	add = InfixOperator(lambda x, y: x + y)
	assert 5 |add| 6 == 11

	decart = InfixOperator(lambda iter1, iter2: [(x, y) for x in iter1 for y in iter2])
	l1 = [1, 2, 3]
	l2 = [4, 5, 6]
	decarted_by_infix = set(l1 |decart| l2)
	decarted_manually = set([(x, y) for x in l1 for y in l2])
	assert decarted_by_infix == decarted_manually
