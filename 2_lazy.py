#!/usr/bin/python

def lazy(decorator):

	def lazyDecorator(decoratee):
		
		# TODO: check how kargs work
		def lazyDecoratee(*args, **kargs):
			return decorator(decoratee)(*args, **kargs)

		return lazyDecoratee

	return lazyDecorator


if __name__ == '__main__':

	def someNormalDecorator(decoratee):
		print 'In some normal decorator'
		return decoratee

	@someNormalDecorator
	def someNormalDecoratee():
		print 'In some normal decoratee'

	@lazy
	def someLazyDecorator(decoratee):
		print 'In some lazy decorator'
		return decoratee

	@someLazyDecorator
	def someLazyDecoratee():
		print 'In some lazy decoratee'

	print 'Calling some normal decoratee'
	someNormalDecoratee()

	print
	print 'Calling some lazy decoratee'
	someLazyDecoratee()