#!/usr/bin/python

"""Decorator that makes function possible to curry"""
class curry:
	
	def __init__(self, func, prevPargs=(), prevKargs={}):

		self.func = func
		func_code = func.func_code

		funcDefArgCount = 0 if func.func_defaults is None else len(func.func_defaults)
		funcMandatoryArgCount = func_code.co_argcount - funcDefArgCount
		self.funcMandatoryArgs = func_code.co_varnames[:funcMandatoryArgCount]

		self.prevPargs = prevPargs
		self.prevKargs = prevKargs


	def __call__(self, *pargs, **kargs):

		allPargs = self.prevPargs + pargs
		allKargs = self.prevKargs.copy()
		allKargs.update(kargs)

		if self.canBeCalled(allPargs, allKargs):
			return self.func(*allPargs, **allKargs)
		else:
			return curry(self.func, allPargs, allKargs)


	def canBeCalled(self, allPargs, allKargs):

		# If there are enough positional args passed - the function can be called
		if len(allPargs) >= len(self.funcMandatoryArgs):
			return True

		# If other mandatory args are in kargs - the function can be called
		mandatoryArgsMaybeInKargs = self.funcMandatoryArgs[len(allPargs):]
		for mandatoryArg in mandatoryArgsMaybeInKargs:
			if mandatoryArg not in allKargs:
				return False

		# Not enough args
		return True


if __name__ == '__main__':

	@curry
	def add(arg1, arg2):
		return arg1 + arg2

	print 'Calling result = add(1,2)'
	result = add(1,2)
	print 'result =', result

	print 'Calling add1 = add(1)'
	add1 = add(1)
	print 'add1 =', add1

	print 'Calling result = add1(2)'
	result = add1(2)
	print 'result = ', result

	print 'Calling result = add1(4)'
	result = add1(4)
	print 'result = ', result

	@curry
	def func(a, b, c=3, d=4, *pargs, **kargs):
		print a, b, c, d, pargs, kargs

	print
	print 'Calling func(1, 2, 3, 4, 5, x=6)'
	func(1, 2, 3, 4, 5, x=6)

	print 'Calling func1 = func(1)'
	func1 = func(1)
	print 'func1 =', func1

	print 'Calling func1(2, 3, 4, 5, x=6)'
	func1(2, 3, 4, 5, x=6)

	print 'Calling func1(2)'
	func1(2)