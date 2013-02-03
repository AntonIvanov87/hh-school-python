#!/usr/bin/python

# fixed all issues:
# tests
# codestyle
# func.__name__, func.__doc__, func.__str__

class Curry:
	"""
	Decorator that makes function possible to curry.
	For example:
	@Curry
	def f(a, b): return a + b
	f1 = f(1)
	f1(2) == 3

	If you begin to curry by arg name - you have to call all rest arguments by name.
	For example:
	f1 = f(b='b')
	f1(a='a') == 'ab'
	"""
	
	def __init__(self, func, prev_pargs=None, prev_kargs=None):

		self.func = func
		self.__name__ = func.__name__ + '_curried'
		self.__doc__ = func.__doc__

		func_code = func.func_code

		func_def_arg_count = 0 if func.func_defaults is None else len(func.func_defaults)
		func_mandatory_arg_count = func_code.co_argcount - func_def_arg_count
		self.func_mandatory_args = func_code.co_varnames[:func_mandatory_arg_count]

		self.prev_pargs = () if prev_pargs is None else prev_pargs
		self.prev_kargs = {} if prev_kargs is None else prev_kargs


	def __call__(self, *pargs, **kargs):

		all_pargs = self.prev_pargs + pargs
		all_kargs = self.prev_kargs.copy()
		all_kargs.update(kargs)

		if self.can_be_called(all_pargs, all_kargs):
			return self.func(*all_pargs, **all_kargs)
		else:
			return Curry(self.func, all_pargs, all_kargs)


	def can_be_called(self, all_pargs, all_kargs):

		# If there are enough positional args passed - the function can be called
		if len(all_pargs) >= len(self.func_mandatory_args):
			return True

		# If other mandatory args are in kargs - the function can be called
		mandatory_args_maybe_in_kargs = self.func_mandatory_args[len(all_pargs):]
		for mandatoryArg in mandatory_args_maybe_in_kargs:
			if mandatoryArg not in all_kargs:
				return False

		return True


	def __str__(self):

		buf = 'function ' + self.__name__
		if self.prev_pargs or self.prev_kargs:
			buf += ' with ' + str(self.prev_pargs) + ', ' + str(self.prev_kargs)
		return buf


if __name__ == '__main__':

	@Curry
	def add(arg1, arg2):
		"""Adds arg1 and arg2"""
		return arg1 + arg2

	assert add.__name__ == 'add_curried'
	assert add.__doc__ == 'Adds arg1 and arg2'
	assert add.__str__() == 'function add_curried'

	add1 = add(1)

	assert add1.__name__ == 'add_curried'
	assert add1.__doc__ == 'Adds arg1 and arg2'
	assert add1(2) == 3
	assert add1(4) == 5

	addb = add(arg2='b')
	assert addb(arg1='a') == 'ab'
	
	@Curry
	def func(a, b, c, d=4, *pargs, **kargs):
		return (a, b, c, d, pargs, kargs)

	func12 = func(1, 2, x=6)
	assert func12(3, 4, 5, y=7) == (1, 2, 3, 4, (5,), {'x': 6, 'y': 7})
	assert func12(3) == (1, 2, 3, 4, (), {'x': 6})