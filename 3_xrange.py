#!/usr/bin/python

"""Almost range, but lazy: generates next number only when needed"""
class xrange(object):

	# TODO: docstring 
	def __init__(self, *args):

		if len(args) == 1:
			self.__init__(*(0, args[0]))
		
		elif len(args) == 2:
			step = 1 if args[0] <= args[1] else -1
			self.__init__(*(args[0], args[1], step))

		elif len(args) == 3:
			self.start = args[0]
			self.stop = args[1]
			self.step = args[2]

		else:
			raise TypeError('Invalid number of args!')
	

	def __iter__(self):

		def iterFunc():
			
			if self.step > 0:
				def continueLoop(i):
					return i < self.stop
			else:
				def continueLoop(i):
					return i > self.stop
			
			i = self.start
			while continueLoop(i):
				yield i
				i += self.step

		return iterFunc()


	def __len__(self):

		diff = self.stop - self.start
		if diff % self.step == 0:
			return diff / self.step
		else:
			return 1 + diff / self.step


	# TODO: slice
	def __getitem__(self, indexOrSliceObject):

		# we can implement __getslice__ but it is not supported in future python vertions
		def getBySlice(sliceObject):

			# we are not fully comply with slice protocol
			# in slice we can choose out of range index
			# but I consider it as an error rather that a feature

			# step
			stepIndex = 1 if sliceObject.step == None else sliceObject.step
			step = self.step * stepIndex

			# start
			if sliceObject.start == None:
				start = self.start if stepIndex >= 0 else self[len(self)-1]
			else:
				start = self[sliceObject.start]

			# stop
			if sliceObject.stop == None:
				stop = self.stop if stepIndex >= 0 else self.start + step
			else:
				stop = self[sliceObject.stop]

			return xrange(start, stop, step)


		def getByIndex(index):

			l = len(self)
			if index >= l or index <= -l:
				raise IndexError('index out of range')

			if index >= 0:
				return self.start + index*self.step
			else:
				return self.start + (l+index)*self.step

		return getBySlice(indexOrSliceObject) if isinstance(indexOrSliceObject, slice) else getByIndex(indexOrSliceObject)
		

	def __contains__(self, what):

		if self.step >=0:

			if what < self.start or what >= self.stop:
				return False

		else:

			if what > self.start or what <= self.stop:
				return False

		return (what - self.start) % self.step == 0



	def __str__(self):

		s = 'xrange(' + str(self.start) + ',' + str(self.stop) + ',' + str(self.step) + '):'
		# it's no good to print all elements, but for learning and testing purposes - it's ok
		for i in self:
			s += ' ' + str(i)
		return s


if __name__ == '__main__':

	def demonstrate(expression):
		print expression + ':', eval(expression)

	print 'contents:'
	demonstrate('xrange(3)')
	demonstrate('xrange(1,3)')
	demonstrate('xrange(1,6,2)')
	demonstrate('xrange(-3)')
	demonstrate('xrange(1,-3)')
	demonstrate('xrange(1,-6,-2)')

	print
	print 'len:'
	demonstrate('len(xrange(1,6,2))')
	demonstrate('len(xrange(1,-6,-2))')
	
	print
	print 'indices:'
	demonstrate('xrange(1,6,2)[1]')
	demonstrate('xrange(1,6,2)[2]')
	demonstrate('xrange(1,6,2)[-1]')
	demonstrate('xrange(1,6,2)[-2]')
	demonstrate('xrange(1,-6,-2)[1]')
	demonstrate('xrange(1,-6,-2)[-1]')

	print 
	print 'in:'
	demonstrate('0 in xrange(1,6,2)')
	demonstrate('1 in xrange(1,6,2)')
	demonstrate('2 in xrange(1,6,2)')
	demonstrate('6 in xrange(1,6,2)')
	demonstrate('0 in xrange(1,-6,-2)')
	demonstrate('-1 in xrange(1,-6,-2)')

	print
	print 'slices:'
	demonstrate('xrange(1, 6, 2)[1:]')
	demonstrate('xrange(1, 6, 2)[:2]')
	demonstrate('xrange(1, 6, 2)[::-1]')
	demonstrate('xrange(1, 6, 2)[2:0:-1]')
	demonstrate('xrange(1, -6, -2)[1:]')
	demonstrate('xrange(1, -6, -2)[:2]')
	demonstrate('xrange(1, -6, -2)[::-1]')
	demonstrate('xrange(1, -6, -2)[2:0:-1]')