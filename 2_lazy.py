#!/usr/bin/python

import functools

# fixed all issues:
# tests
# repr
# codestyle
# decorators with parameters

def lazy(decorator):
	"""
	Decorator that makes other decorators without parameters lazy.
	Can be useful if decorator uses some global var:
	lazy decorator will use the value of the global var on call time, not on compile time.
	"""

	@functools.wraps(decorator)
	def fake_decorator(decoratee):
		
		@functools.wraps(decoratee)
		def fake_decoratee(*pargs, **kargs):
			return decorator(decoratee)(*pargs, **kargs)

		return fake_decoratee

	return fake_decorator


def lazy_with_params(decorator_with_params):
	"""
	Decorator that makes other decorator with parameters lazy.
	"""

	@functools.wraps(decorator_with_params)
	def fake_decorator_with_params(*dec_pargs, **dec_kargs):

		def fake_decorator(decoratee):
		
			@functools.wraps(decoratee)
			def fake_decoratee(*pargs, **kargs):
				return decorator_with_params(*dec_pargs, **dec_kargs)(decoratee)(*pargs, **kargs)

			return fake_decoratee

		return fake_decorator

	return fake_decorator_with_params


if __name__ == '__main__':

	# test lazy
	decorator_was_called = False

	@lazy
	def some_lazy_decorator(decoratee):
		global decorator_was_called
		decorator_was_called = True
		return decoratee

	@some_lazy_decorator
	def some_lazy_decoratee():
		pass

	assert decorator_was_called == False
	some_lazy_decoratee()
	assert decorator_was_called == True


	# test lazy_with_params
	decorator_was_called = False

	@lazy_with_params
	def some_lazy_decorator_with_params(param1, param2):
		global decorator_was_called
		decorator_was_called = True
		return lambda decoratee: decoratee

	@some_lazy_decorator_with_params('a', 'b')
	def some_lazy_decoratee_2():
		pass

	assert decorator_was_called == False
	some_lazy_decoratee_2()
	assert decorator_was_called == True
