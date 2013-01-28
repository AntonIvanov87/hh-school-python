#!/usr/bin/python

import functools

def lazy(decorator):
	"""
	Decorator that makes other decorators lazy.
	Can be useful if decorator uses some global var:
	lazy decorator will use the value of the global var on call time, not on compile time.
	Do not support decorators with args yet.
	"""

	@functools.wraps(decorator)
	def lazy_decorator(decoratee):
		
		@functools.wraps(decoratee)
		def lazy_decoratee(*args, **kargs):
			return decorator(decoratee)(*args, **kargs)

		return lazy_decoratee

	return lazy_decorator


if __name__ == '__main__':

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