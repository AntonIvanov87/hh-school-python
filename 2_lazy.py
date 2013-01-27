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
	def lazyDecorator(decoratee):
		
		@functools.wraps(decoratee)
		def lazyDecoratee(*args, **kargs):
			return decorator(decoratee)(*args, **kargs)

		return lazyDecoratee

	return lazyDecorator


if __name__ == '__main__':

	decoratorWasCalled = False

	@lazy
	def someLazyDecorator(decoratee):
		global decoratorWasCalled
		decoratorWasCalled = True
		return decoratee

	@someLazyDecorator
	def someLazyDecoratee():
		pass

	assert decoratorWasCalled == False
	someLazyDecoratee()
	assert decoratorWasCalled == True