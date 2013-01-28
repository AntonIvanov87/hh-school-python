#!/usr/bin/python

class xrange(object):
	"""
	Almost range, but lazy: generates next number only when needed.
	"""

	def __init__(self, start_stop, stop=None, step=1):

		if stop is None:
			self.start = 0
			self.stop = start_stop

		else:
			self.start = start_stop
			self.stop = stop

		self.step = step
	

	def __iter__(self):

		def iter_func():
			
			i = self.start
			while i < self.stop if self.step >=0 else i > self.stop:
				yield i
				i += self.step

		return iter_func()


	def __len__(self):

		diff = abs(self.stop - self.start)
		if diff % self.step == 0:
			return diff / abs(self.step)
		else:
			return 1 + diff / abs(self.step)


	def __getitem__(self, index_or_slice):

		# we can implement __getslice__ but it is not supported in future python vertions
		def get_by_slice(slice_object):

			# we are not fully comply with slice protocol
			# in slice we can choose out of range index
			# but I consider it as an error rather that a feature

			# step
			step_index = 1 if slice_object.step == None else slice_object.step
			step = self.step * step_index

			# start
			if slice_object.start == None:
				start = self.start if step_index >= 0 else self[len(self)-1]
			else:
				start = self[slice_object.start]

			# stop
			if slice_object.stop == None:
				stop = self.stop if step_index >= 0 else self.start + step
			else:
				stop = self[slice_object.stop]

			return xrange(start, stop, step)


		def get_by_index(index):

			l = len(self)
			if index >= l or index <= -l:
				raise IndexError('index out of range')

			if index >= 0:
				return self.start + index*self.step
			else:
				return self.start + (l+index)*self.step

		return get_by_slice(index_or_slice) if isinstance(index_or_slice, slice) else get_by_index(index_or_slice)
		

	def __contains__(self, what):

		if self.step >=0:

			if what < self.start or what >= self.stop:
				return False

		else:

			if what > self.start or what <= self.stop:
				return False

		return (what - self.start) % self.step == 0



	def __str__(self):

		return 'xrange(' + str(self.start) + ',' + str(self.stop) + ',' + str(self.step) + ')'


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