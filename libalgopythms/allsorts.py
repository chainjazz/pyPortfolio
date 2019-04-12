# -*- coding: UTF-8 -*-

from random import randint as rand
import time
import sys

def sort_merge(iterable, size):
	swaps = 0
		
	for i in range(0,size,2):
		for j in range(2):				
			if iterable[i] < iterable[i+j]:
				break
			else:
				swaps += 1
				swap = iterable[i]
				iterable[i] = iterable[i+j]
				iterable[i+j] = swap
	
	print iterable
	
	swaps = 0
	
	for i in range(0, size, 4):		
		val1 = iterable[i] 
		val2 = iterable[i+1]
		
		val3 = iterable[i+2] 
		val4 = iterable[i+3]
				
		if not val1 < val3: 
			swaps += 1
		else:
			iterable[i] = val3 # < val2
			iterable[i+1] = val1 # < val4
			
		if not val2 < val4:
			swaps += 1
			iterable[i+2] = val4
			iterable[i+3] = val2
			
	print iterable
	
	swaps = 0
	
	for i in range(0, size, 8):
		val1 = iterable[i] # < val2 < val3 < val4
		val2 = iterable[i+1]		
		val3 = iterable[i+4]
		val4 = iterable[i+5]
		
		val5 = iterable[i+2] # < val6 < val7 < val8
		val6 = iterable[i+3]		
		val7 = iterable[i+6] 
		val8 = iterable[i+7]
		
		if not val1 < val5: # and < val6+
			swaps += 1
			iterable[i] = val5 # < val4+
			iterable[i+1] = val1 # < val6+
					
		if not val2 < val6: # and < val6+
			swaps += 1
			iterable[i+2] = val6 # < val4+
			iterable[i+3] = val2 # < val6+
					
		if not val3 < val7: # and < val6+
			swaps += 1
			iterable[i+4] = val7 # < val4+
			iterable[i+5] = val3 # < val6+
					
		if not val4 < val8: # and < val6+
			swaps += 1
			iterable[i+6] = val8 # < val4+
			iterable[i+7] = val4 # < val6+
						
	print iterable	

def sort_bubble(iterable, size):	
	swaps = 0 # swap count (sentinel)
	
	for i in range(size - 1):
		val1 = iterable[i]
		val2 = iterable[i+1]
						
		if val1 < val2:			
			continue # skip sorted pairs
		else: # swap
			swaps += 1
			iterable[i] = val2
			iterable[i+1] = val1		
	
	if swaps == 0:
		# print swaps
		return
	else:
		# print no_swaps
		# recurse
		sort_bubble(iterable, size - 1)
		
	
		
# ##################		
# ###########   TEST 
# ##################

rtstart = 0	
rtdelta = 0
tdelta = 0
tavg = 0
scalars = [rand(0,8) for x in range(65535)]
items = []
nitems = 8

rtstart = time.clock()

for i in range(1): # range(65535 / nitems):
	items = scalars[i*nitems:i*nitems+nitems]

	try:
		rtdelta = time.clock() - rtstart
		sort_merge(items, len(items))
		tdelta = time.clock() - rtdelta
		tavg += tdelta
	except RuntimeError, msg:
		print u"Too many recursions (", msg, ")"
		break
	
	
			
	if items[:5] != sorted(items[:5]):
		print "ERROR"
		break
	
	
		
print u'Sorted %d items %d times,\n \
%.4f ms avg per sort, r-limit %d,\n \
%d seconds overall'.encode('utf-8') % \
		(nitems, 65535 / nitems, 
			(tavg * 1000 ) / nitems, 
			sys.getrecursionlimit(),
			(time.clock() - rtstart ) + 1)
	
	
	

	


