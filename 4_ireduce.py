#!/usr/bin/python

"""As reduce but yields a number on each reduce iterations.
Can be useful for example to show modification of some indicator during reduce process."""
def ireduce(func, iterable, init=None):

	iterator = iter(iterable)
	
	if init == None:
		try:
			init = next(iterator)
		except StopIteration:
			raise TypeError('Empty iterable and no init value!')
	
	acc = init

	for i in iterator:
		acc = func(acc, i)
		yield acc


if __name__ == '__main__':

	print 'ireduce(add, [1, 2, 3]):'
	l = [1, 2, 3]
	for i in ireduce(lambda a, b: a+b, l):
		print i

	print
	print 'ireduce(add, ["a", "b", "c"])'
	l = ['a', 'b', 'c']
	for i in ireduce(lambda a, b: a+b, l):
		print i
