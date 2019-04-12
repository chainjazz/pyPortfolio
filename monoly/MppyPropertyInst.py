'''
Created on 22.12.2015.

@author: dkr85djo
'''
import struct
from MppyProperty import MppyProperty

class MppyPropertyInst(MppyProperty):
    '''
    classdocs
    '''


    def __init__(self, i):
        '''
        Constructor
        '''
        
        super(MppyPropertyInst, self).__init__()
        self.id = i # id of property, start from 1
        self.ownedby = 0 # id of player
        self.devlevel = 0 # development level - id of property development state
                                # such as
                                # 0 = undeveloped
                                # 1 = owned
                                # 2 = colourgrouped (when all of group is owned by same player)
                                # 3 = 1 house
                                # 4 = 2 houses
                                # 5 = 3 houses
                                # 6 = hotel
        self.grplevel = 0 # property instance colourgroup level reached (based on nitems)
        self.mortgage = 0 # binary if mortgaged
        
        
    def net_setall(self, tdata):
        self.ownedby = tdata[2]
        self.devlevel = tdata[3]
        self.grplevel = tdata[4]
        self.mortgage = tdata[5]
    
    def net_getall(self):
        return struct.pack("!5L", 
                        self.id,
                        self.ownedby,
                        self.devlevel,
                        self.grplevel,
                        self.mortgage)
        