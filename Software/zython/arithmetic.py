import numpy as np


def gcd(a,b):
	"""
	This function performs greatest common divisor on each element of a,b array.
	a: numpy array
	b: numpy array
	"""
	def _gcd(_a,_b):
		while _b:
			_a,_b = _b,_a%_b
		return _a
	_gcd_vec = np.vectorize(_gcd)
	return _gcd_vec(a,b)