import random
import math

players = [float(1.0 / 11) for x in range(11)]
passes = [0 for x in range(11)]
recivs = [0 for x in range(11)]
pnames = [u"Rastko", u"Krava", u"Mama", u"Tata", u"Alex", u"Maja", u"Mirna",
	u"Rasa", u"Tina", u"Larisa", u"Jay Kay"]

i = 0
npasses = 1444
passer = 0
receiver = 0
alltime = [0]
rankdelta = 0
rankadjust = 0
favplayer = 0

while i < npasses:
	passer = random.randint(0,10)
	receiver = random.randint(0,10)
	
	if passer == receiver:
		continue
	
	players_sorted = players	
	favplayer = max(players)	
	rankdelta = players[passer] / 11
	rankadjust = rankdelta / 9
	
	if favplayer > players_sorted[alltime[-1]]:
		alltime.append(players_sorted.index(favplayer))
		print "new alltime ", pnames[alltime[-1]]
	
	
	players_sorted[receiver] += rankdelta	
	
	for x in range(11):		
		if x != receiver and x != passer:
			players_sorted[x] -= rankadjust			
		elif x == receiver:			
			recivs[x] += 1
		else:
			passes[x] += 1
	
	if round(sum(players)) != 1.0:
		print "ERROR"
		print round(sum(players))
		break
		
	
	players = players_sorted	
	i = i + 1	


for x in alltime:
	print '%s %d %d %4.3f' % (pnames[x], 
		recivs[x], 
		passes[x],
		players[x])