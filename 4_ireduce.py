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

	iterator = ireduce(lambda x, y: x+y, [1, 2, 3])
	assert next(iterator) == 3
	assert next(iterator) == 6

	iterator = ireduce(lambda x, y: x+y, ['a', 'b', 'c'])
	assert next(iterator) == 'ab'
	assert next(iterator) == 'abc'