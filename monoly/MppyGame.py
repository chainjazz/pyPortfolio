'''
Created on 22.12.2015.

@author: dkr85djo
'''
import socket
import struct
from MppyPlayer import MppyPlayer

class MppyGame(object):
    '''
    classdocs
    '''


    def __init__(self, nplayers):
        '''
        Constructor
        '''
        self.nplayers = nplayers; # num of players (max num for net)
        self.aplayers = 0 # number of active players, 1 = game won
        self.turn = 0
        self.tcount = 0 # turn count
        self.ecount = 0 # event count (card iterator)        
        self.conn = 0 # player connections
        self.nconns = 0
        
    def advance_turn(self):
        if (self.aplayers): # turn is 1-based counter; thus the weirdness
            self.turn = ((self.turn - 1 + 1) % self.aplayers) + 1
            # id of player whose turn it is now
            
    def net_waitforplayers(self, players):
        self.conn = socket.socket(type=socket.SOCK_DGRAM)
        self.conn.bind(('127.0.0.1', 8088))        
        
        try:
            while self.aplayers < self.nplayers:
                #self.conn.listen()
                (b, a) = self.conn.recvfrom(124)
                self.aplayers = self.aplayers + 1
                players.append(MppyPlayer(self.aplayers))
                players[self.aplayers - 1].conn = a
                players[self.aplayers - 1].name = b.decode()
                
                self.net_scdmsg(players[self.aplayers - 1],
                                 ("Hi, " + b.decode()))
                
                if (self.aplayers > 1):
                    c = input ("Wait for more? [n] ")
                    
                    if c == '' or c == 'n':
                        # TODO: figure out what this is
                        for d in players:
                            self.conn.sendto(struct.pack("!2L120s", 0x4, self.aplayers, " ".encode()), d.conn)
                        
                        for p in players:
                            self.net_scdplayer(players, p)                           
                        
                        self.nplayers = self.aplayers
                
        except KeyboardInterrupt:
            for c in players:
                c.conn.shutdown(socket.SHUT_RDWR)
                c.conn.close()
                
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn.close()
            print ("Game hasn't started. Exiting.")
    
    # net_s(ync)c(lient)d(ata)player
    def net_scdplayer(self, cli, player):       
        
        for d in cli:
            self.conn.sendto(struct.pack("!L24s100s", 0x1, player.net_getall(), b" "), d.conn)
            
            
    def net_scdprops(self, cli, prop):
        for d in cli:
            self.conn.sendto(struct.pack("!L20s104s", 0x2, prop.net_getall(), b" "), d.conn)
    
    def net_scdgame(self, cli):
        
        for d in cli:
            self.conn.sendto(struct.pack("!L16s108s", 0x3, self.net_getall(), b" "), d.conn)
        
    def net_scdmsg(self, cli, msg):
        self.conn.sendto(struct.pack("!L124s", 0x0, msg.encode()), cli.conn)
        
    def net_setall(self, tdata):
        self.aplayers = tdata[1]
        self.turn = tdata[2]
        self.ecount = tdata[3]
        self.tcount = tdata[4]
        
    def net_getall(self):
        return struct.pack("!4L", self.aplayers,
                           self.turn,
                           self.ecount,
                           self.tcount)                
            
    def game_loop(self, players, fields, props, events):
        try:
            while self.aplayers > 1:
                cp = players[self.turn - 1] # current player pointer
                ce = events[self.ecount % len(events)]  
                pf = fields[cp.position - 1]

                self.net_scdmsg(cp, str(cp.balance) + ","
                                    + str(cp.wanted) + ","
                                    + str(cp.jailed) + ","
                                    + str(cp.position) + "\n")
                
                # TODO: convert to "net_input"
                # funkcija koja vrsi autorizaciju klijenata
                # i ceka na unos podataka/poruka kada je to potrebno
                a = input("? ")

                if a == "" or a == "r":
                    cp.adv_pos(cp.roll_dice(), len(fields))                
                    pf = fields[cp.position - 1]
                    
                    if pf.type == 5:
                        cp.jailed = 1
                        cp.wanted = 3
                        cp.adv_pos(-20, len(fields))
                    elif pf.type == 2:
                        ce.evt_play(fields, players, props, self)
                        self.ecount = (self.ecount + 1) % len(events)                  
                                    
                if cp.jailed == 1:
                    self.advance_turn()
                elif cp.wanted == 0:
                    self.advance_turn()
                    
                self.tcount = self.tcount + 1
                
                
        except KeyboardInterrupt:
            print ("You pressed Ctrl+C")