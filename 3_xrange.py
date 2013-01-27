#!/usr/bin/python

"""Almost range, but lazy: generates next number only when needed"""
class xrange(object):

	def __init__(self, startStop, stop=None, step=1):

		if stop is None:
			self.start = 0
			self.stop = startStop

		else:
			self.start = startStop
			self.stop = stop

		self.step = step
	

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

		diff = abs(self.stop - self.start)
		if diff % self.step == 0:
			return diff / abs(self.step)
		else:
			return 1 + diff / abs(self.step)


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

	assert len(xrange(3)) == 3
	assert len(xrange(1,3)) == 2
	assert len(xrange(1, 6, 2)) == 3
	assert len(xrange(-3)) == 3
	assert len(xrange(1, -3)) == 4
	assert len(xrange(1, -6, -2)) == 4
	
	assert xrange(3)[0] == 0
	assert xrange(3)[-1] == 2
	assert xrange(1, 3)[0] == 1
	assert xrange(1, 3)[-1] == 2
	assert xrange(1, 6, 2)[0] == 1
	assert xrange(1, 6, 2)[1] == 3
	assert xrange(1, 6, 2)[2] == 5
	assert xrange(1, 6, 2)[-1] == 5
	assert xrange(1, 6, 2)[-2] == 3
	assert xrange(1, -6, -2)[1] == -1
	assert xrange(1, -6, -2)[-1] == -5

	assert 0 not in xrange(1, 6, 2)
	assert 1 in xrange(1, 6, 2)
	assert 2 not in xrange(1, 6, 2)
	assert 6 not in xrange(1, 6, 2)
	assert 0 not in xrange(1, -6, -2)
	assert -1 in xrange(1, -6, -2)

	assert xrange(1, 6, 2)[1:][0] == 3
	assert xrange(1, 6, 2)[1:][-1] == 5
	assert xrange(1, 6, 2)[:2][0] == 1
	assert xrange(1, 6, 2)[:2][-1] == 3
	assert xrange(1, 6, 2)[::-1][0] == 5
	assert xrange(1, 6, 2)[::-1][-1] == 1
	assert xrange(1, 6, 2)[2:0:-1][0] == 5
	assert xrange(1, 6, 2)[2:0:-1][-1] == 3