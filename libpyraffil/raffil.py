import socket as ipc
import signal
import sys

class InetServeL:
	def __init__(self, bsize, port):
		self.n = bsize
		self.p = port
		self.i = 0
		self.q = 0
		self.c = 0
		self.s = 0
		#signal.signal(signal.SIGINT,self.int_handler)
		
	def int_handler(self, sig, frame):
		print "Exception caught, exiting cleanly."
		self.stopListen()
		sys.exit(0)	
	
	def respond2Request(self):
		self.i.shutdown(1)
	
	def startListen(self):
		self.s = ipc.socket(ipc.AF_INET, ipc.SOCK_STREAM, 0)
		self.s.bind(('localhost', self.p))
		self.s.listen(1)
		
		while 1:
			try:
				(self.i, self.c) = self.s.accept()
				self.q = self.i.recv(self.n)
				self.respond2Request()
			except KeyboardInterrupt:
				self.int_handler(0,0)
			
	def stopListen(self):
		self.i.shutdown(0);
		self.s.close();