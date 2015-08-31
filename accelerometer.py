from adxl345 import ADXL345
from collections import deque
from itertools import izip
from util import axis_dict_to_tuple
import numpy


adxl345 = ADXL345()

def acel_reader(window_size=3):
	window = [deque([0] * window_size, maxlen=window_size) for _ in ('x', 'y', 'z')]
	while True:
		reading = axis_dict_to_tuple(adxl345.getAxes(True))
		for latest_reading, axis_dequeue in izip(reading, window):
			axis_dequeue.append(latest_reading)
		yield (numpy.mean(axis_dequeue) for axis_dequeue in window)

class Accelerometer(object):
	""" A singleton class to yield buffered readings from the accelerometer """

	__instance = None

	def __new__(cls, window_size=10):
		if Accelerometer.__instance is None:
			Accelerometer.__instance = object.__new__(cls)
		Accelerometer.__instance._accel_reader = acel_reader(window_size)
		return Accelerometer.__instance

	def __iter__(self):
		return self

	def next(self):
		return tuple(self._accel_reader.next())

	def __next__(self):
		return self.next()
