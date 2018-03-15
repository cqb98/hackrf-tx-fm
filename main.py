import pylibhackrf ,ctypes
import queue
import time
import numpy
import math
import sys
import pyaudio
import threading
import pyaudio2iq

hackrf = pylibhackrf.HackRf()
a2iq=pyaudio2iq.audio2iq()

DACfreq=int(2.56e6)
if hackrf.is_open == False:
	hackrf.setup()
	if(len(sys.argv)>=2):
		hackrf.set_freq(int(float(sys.argv[1])))
	else:
		hackrf.set_freq(int(99.4e6))
	hackrf.set_sample_rate(DACfreq)
	hackrf.set_amp_enable(False)
	hackrf.set_lna_gain(40)
	hackrf.set_vga_gain(62)	
	hackrf.set_txvga_gain(47);

count=0
def callback_fun(hackrf_transfer):
	global count,times,q,a2iq,delta
	buffer_length=int(hackrf_transfer.contents.buffer_length);
	length=buffer_length//2
	
	array_type = (ctypes.c_byte*hackrf_transfer.contents.buffer_length)
	values = ctypes.cast(hackrf_transfer.contents.buffer, ctypes.POINTER(array_type)).contents

	pos=0;
	while(not q.empty()):
		if((pos+delta)>length):
			break
		vals=q.get()
		pos+=a2iq.a2iq(vals,len(vals),1,values,pos,127,times)
	print("txLen=%d\tcount=%d\tpos=%d\tdelta=%d"%(length,count,pos,delta));
	count=count+1
	return 0


RATE=40000
CHUNK=2048
times=int(DACfreq/RATE)
q=queue.Queue()
delta=CHUNK*times
def audio_get():
	global RATE,CHUNK;
	FORMAT=pyaudio.paInt16
	CHANNELS=1
	p=pyaudio.PyAudio();
	s=p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK);
	while(1):
		data=s.read(CHUNK);
		f=list(map(lambda x:x/32768,numpy.frombuffer(data,numpy.dtype('<i2'))));
		q.put(f)
		#print(f)
		
threading.Thread(target=audio_get).start()
hackrf.start_tx_mode(callback_fun)
