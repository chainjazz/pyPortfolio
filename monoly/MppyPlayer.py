'''
Created on 22.12.2015.

@author: dkr85djo
'''
import random
import struct

class MppyPlayer(object):
    '''
    classdocs
    '''


    def __init__(self, i):
        '''
        Constructor
        '''
        self.position = 0 # id of game board field (to be re-defined in boardless terms)
        self.balance = 1500
        self.id = i # default 0, means inactive; active players start from 1
        self.wanted = 0 # wanted level, roll counter to get in/out of jail
        self.jailed = 0 # true if jailed
        self.immune = 0 # holder of "get out of jail" card
        self.name = "Player" + str(self.id)
        
        self.conn = 0 # socket object for net connection
        
    def adv_pos(self, deltapos, nfields):
        newpos = self.position + deltapos
        
        if newpos > nfields:
            self.balance = self.balance + 200
            newpos = newpos % nfields            
        
        self.position = newpos
        
    def roll_dice(self):
        do = random.randint(1, 6)
        dt = random.randint(1, 6)
        
        if dt == do:
            if self.jailed == 0:
                self.wanted = self.wanted + 1
            else:
                self.wanted = 1
                self.jailed = 0           
        
        elif dt != do:
            if self.jailed == 0:
                self.wanted = 0
            else:
                self.wanted = self.wanted - 1                
                
        if self.wanted == 0:
            self.jailed = 0
        elif self.wanted == 3:
            self.jailed = 1
            self.position = 11
            return 0
                
        if self.jailed == 0:
            return dt + do
        else:
            self.position = 11
            return 0
        
        
    def net_setall(self, tdata):
        self.position = tdata[1]
        self.balance = tdata[2]
        #self.id = tdata[3]
        self.wanted = tdata[4]
        self.jailed = tdata[5]
        self.immune = tdata[6]
        
    def net_getall(self):
        return struct.pack("!6L",# type of data
                        # 0x1 = player data
                        # 0x2 = props data
                        # 0x3 = game data
                        self.position,
                        self.balance,
                        self.id,
                        self.wanted,
                        self.jailed,
                        self.immune)
                
                
                
                
                
                