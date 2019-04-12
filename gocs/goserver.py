from socket import *
from pickle import *
import golib

# NOTE
# TODO
# Combine server and client code into one module and
# use run-time logic to switch between the two
# The codes are not that much different

# CONSTANTS

dmn = 19
fds = dmn * dmn
fra = 30 # stone radius in pixels

# GLOBALS

h = '192.168.1.100'
p = 8088

cmn = "" # command buffer remote

pls = [0, 0] # player data
brd = golib.brd # the board
win = 0 # win condition, actually, a pass counter; if > 2(1), end game
trn = 0 # turn looping counter
cpl = 0 # player counter
sms = "" # server feedback text


#TODO
# assuming clients have different ip's (for testing, use
#   local and dynamic-DNS host addresses) we can differentiate
#   players by ip, such that we compare the ip with the index
#   of the player (in this case, 2 players), and update corresponding
#   player's stats, filter-out illegal input, etc.

class goPlayer:
    def __init__(self, inip):
        self.inip = inip # ip address of player, see above
                            # additional note: the client gets
                            # a random "talk-back" port that will
                            # probably be different for each client
                            # even if the ip's the same, but this is
                            # most likely dependent on extrenal factors
        self.csto = 0
        self.psto = fds / 2

def getTurn():
    return trn % 2

def passMove(): 
    global win, trn
    
    if win < 2:
        win += 1 # increment pass counter
        trn += 1 # it's a valid move
        #UpdateBoardGui()
    
        #TODO: calculate score

def placeMove(n): # remove args once we move binding to terminal
    global brd, win, trn, pst
    # input board field or pass     
    adv = trn # set "advance move flag" to current turn
    #print "Turn " + str(trn / 2 + 1) + ", pass " + str(win) + " / 2"       
    
    win = 0 # if not passing, break pass "chain" (max 2)
            
    if brd[n] == 0: # if selected field is empty
        brd[n] = (getTurn() + 1) # set board field to player piece
        pls[getTurn()].psto = pls[getTurn()].psto - 1 # decrement player stash
        trn = trn + 1 # increment turn
    else:
        print "Invalid move, try again"

    golib.CheckBoard()

def OnExitGui():
    pass




try:
    lesock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    lesock.bind((h, p))
except error, (s):
    print s

# block until 2 players, then unblock (or not)
lesock.setblocking(1)
 

while win < 2:
    cmn = ""
    
    while cmn == "":
        try:
            cmn = lesock.recvfrom(256)
        except error, (s):
            #print s
            break

        pcm = loads(cmn[0]) # cmn[0] = data, cmn[1] = ipaddr
       
        if pcm[0] == "PLACE":
            if cpl == 2 and cmn[1] == pls[getTurn()].inip:
                placeMove(pcm[1])
        elif pcm[0] == "PASS":
            if cpl == 2 and cmn[1] == pls[getTurn()].inip:
                passMove()
        elif pcm[0] == "ADDPL":
            if cpl < 2: # if player count < 2
                cpl = cpl + 1 # increment player count
                pls[cpl - 1] = goPlayer(cmn[1]) # instantiate player
                print "Added " + str(cmn[1]) + " as player " + str(cpl)
        else:
            pass

        lesock.sendto(dumps(brd), cmn[1])
        print "Received " + str(len(cmn)) + " B from " + str(cmn[1][0]) #DBG


try:
    lesock.close()
except error, (s):
    print s


