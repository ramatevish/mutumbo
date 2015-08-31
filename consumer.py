import time
from features import euclidean_distance


class Consumer(object):

	def __init__(self, reader):
		self.reader = reader

	def loop(self):
		pass


class KnockDetectingConsumer(object):

	def __init__(self, reader, on_knock):
		self.reader = reader
		self.on_knock = on_knock
		self._last_knock = 0.00000001
	
	def loop(self):
		for _ in xrange(3):  # prime the pump
			self.reader.next()

		a0, a1 = self.reader.next(), self.reader.next()
		for reading in self.reader:
			cur_time = time.time()
			a1, a0 = a0, reading
			if abs(euclidean_distance(a0, a1)) > .05:
				if self._last_knock and (cur_time - self._last_knock) > 3:
					print "%.2f KNOCK KNOCK MOTHERFUCKER" % cur_time
					self.on_knock()
					self._last_knock = cur_time
					
			time.sleep(.001)
