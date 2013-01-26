#!/usr/bin/python

"""Allows to simulate infix operators"""
class InfixOperator:

	"""func - function to be called on two arguments"""
	def __init__(self, func):

		self.func = func


	def __ror__(self, other):

		return InfixOperatorWithLeftArg(self.func, other)


"""Service class that supports InfixOperator"""
class InfixOperatorWithLeftArg:

	def __init__(self, func, leftArg):

		self.func = func
		self.leftArg = leftArg


	def __or__(self, other):

		return self.func(self.leftArg, other)


if __name__ == '__main__':

	def demonstrate(expression):

		print expression +':', eval(expression)


	add = InfixOperator(lambda x, y: x + y)
	demonstrate('5 |add| 6')

	decart = InfixOperator(lambda iter1, iter2: [(x, y) for x in iter1 for y in iter2])
	demonstrate('[1, 2, 3] |decart| [4, 5, 6]')
