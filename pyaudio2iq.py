import ctypes

class audio2iq(object):
	def __init__(self):
		self.lib=ctypes.CDLL('audio2iq.dylib');
		self.lib.audio2iq.restype=ctypes.c_int
	def a2iq(self,au,length,band,iq,iqOffset,max,times):
		audio=(ctypes.c_double*length)()
		for i in range(length):
			audio[i]=au[i]
		return self.lib.audio2iq(audio,ctypes.c_int(length),ctypes.c_double(band),iq,ctypes.c_int(iqOffset),ctypes.c_char(max),ctypes.c_int(times))
