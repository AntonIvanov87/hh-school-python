#/usr/bin/python

class curry:
	
	def __init__(self, func, prevArgs=()):

		self.func = func
		self.funcNumOfArgs = func.func_code.co_argcount
		self.prevArgs = prevArgs

	def __call__(self, *args):

		allArgs = self.prevArgs + args
		if len(allArgs) < self.func.func_code.co_argcount:
			return curry(self.func, allArgs)
		else:
			return self.func(*allArgs)


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