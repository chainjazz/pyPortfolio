#import msvcrt
from MppyGame import MppyGame
from MppyPropertyInst import MppyPropertyInst
from MppyEvent import MppyEvent
from MppyField import MppyField

# f(ile)init(ialize)events
#
def mppy_finitevents(p, s):
    f = 0
    b = 0
    
    try:
        f = open(s, "r")
    except OSError:
        print ("Error opening file")
        return 0
    

    for line in f:
        vals = line.split(maxsplit=3) #TABS are NOT allowed
        p.append(MppyEvent(b + 1))
        p[b].type = int(vals[0])
        p[b].param1 = int(vals[1])
        p[b].param2 = int(vals[2])
        p[b].desc = vals[3]
        b = b + 1

    f.close()
    
    return b

# f(ile)init(ialize)fields
#
def mppy_finitfields(p, s):
    f = 0
    b = 0
    
    try:
        f = open(s, "r")
    except OSError:
        print ("Error opening file")
        return 0

    for line in f:
        vals = line.split(maxsplit=1)
        p.append(MppyField(b + 1))
        p[b].type = int(vals[0])
        p[b].propertyid = int(vals[1])
        b = b + 1

    f.close()
    
    return b

# f(ile)init(ialize)prop(ertie)s
#
def mppy_finitprops(p, s):
    f = open(s, "r")
    b = 0

    for line in f: # we can iterate over lines in file objects in Py
        vals = line.split(maxsplit=10) # tokenize line string
        p.append(MppyPropertyInst(b + 1))
        p[b].price = int(vals[0])
        p[b].revenue[1] = int(vals[1])
        p[b].revenue[2] = int(vals[2])
        p[b].revenue[3] = int(vals[3])
        p[b].revenue[4] = int(vals[4])
        p[b].revenue[5] = int(vals[5])
        p[b].revenue[6] = int(vals[6])
        p[b].colourgroup = int(vals[7])
        p[b].maxdevlevel = int(vals[8])
        p[b].maxgrplevel = int(vals[9])
        p[b].name = vals[10]        
        b = b + 1

    f.close()
    
    return b


def mppy_updatedisplay(fields, players, props, game, events):
    pf = 0 # cp field desc pointer
    
    # MAKE SURE this printout reflects the state of the game
    # since its a separate function   
    
    for cp in players:
        pf = fields[cp.position - 1] # current player field desc pointer
        le = events[game.ecount - 1]
        
        if cp.id != 0:
            if cp.id == game.turn:
                print ("*", end=' ')
            print (cp.name + "(" + str(cp.balance) + "," 
                   + str(cp.position) + "," 
                   + str(cp.wanted) + ","
                   + str(cp.jailed) 
                   + ") is", end=' ')        
            if pf.type == 1:
                print ("at " + props[pf.propertyid - 1].name)
            elif pf.type == 2:
                print ("-*-" + le.desc + "(" + str(le.param1) + ")")
            elif pf.type == 3:
                if cp.jailed == 0:
                    print ("just passing by...")
                else:
                    print ("in jail :(")
            elif pf.type == 4:
                print ("lucky!")
            elif pf.type == 5:
                print ("!LOGICAL PROGRAM ERROR")
            elif pf.type == 6:
                print ("taxed.")
            elif pf.type == 7:
                print ("at START.")
                


    

def mppy_start():
    
    players = []
    props = []
    fields = []
    gevents = []
    dagame = MppyGame(2) #arg = max players allowed
    
    mppy_finitprops(props, "props.txt")
    mppy_finitevents(gevents, "gevents.txt")
    mppy_finitfields(fields, "fields.txt")

    '''

    while b < dagame.nplayers:
        players.append(MppyPlayer(b + 1))
        players[b].position = 1
        print (players[b].name)
        b = b + 1
        
    '''
    print ("Waiting for players...")
    dagame.net_waitforplayers(players)
    #dagame.aplayers = dagame.nplayers
    dagame.turn = 1
    print ("Starting game...")
    dagame.game_loop(players, fields, props, gevents)
    
    print ("Stopping server.")    
    
    '''
    player in jail can
    
    roll dice
        continues playing as usual if he gets doubles
    purchase an immunity card (GOOJF) from another on his turn
        continues playing as usual
    pay 50 BEFORE rolling dice
        continues playing as usual
    wait three turns
        pays 50 unless throwing doubles 
        continues playing as usual
        
    work with properties as usual    
    '''

        



mppy_start()
        

