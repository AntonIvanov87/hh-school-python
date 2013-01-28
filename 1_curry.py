#!/usr/bin/python

class Curry:
	"""
	Decorator that makes function possible to curry.
	Does not support decorating class methods yet.
	"""
	
	def __init__(self, func, prev_pargs=None, prev_kargs=None):

		self.func = func
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

		# Not enough args
		return True


if __name__ == '__main__':

	@Curry
	def add(arg1, arg2):
		return arg1 + arg2

	add1 = add(1)
	assert add1(2) == 3
	assert add1(4) == 5

	@Curry
	def func(a, b, c=3, d=4, *pargs, **kargs):
		return (a, b, c, d, pargs, kargs)

	func1 = func(1)
	assert func1(2, 3, 4, 5, x=6) == (1, 2, 3, 4, (5,), {'x': 6})
	assert func1(2) == (1, 2, 3, 4, (), {})