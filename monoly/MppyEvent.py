'''
Created on 23.12.2015.

@author: dkr85djo
'''

class MppyEvent(object):
    '''
    classdocs
    '''
    
    def __init__(self, i):
        '''
        Constructor
        '''
        self.id = i
        self.type = 0 # 1 = GOOJF, 
                        # 2 = positional
                        # 3 = monetary
                        # 4 = GTJ
                        # 5 = switch event (card)
                        # 6 = birthday
                        # 7 = repairs
        self.param1 = 0
        self.param2 = 0
        self.desc = "Undefined"
    
    def evt_play(self, fields, players, props, game):
        nfields = len(fields)
        cp = players[game.turn - 1]       
        
        if self.type == 1:
            cp.immune = 1
        elif self.type == 2:
            if self.param1 == 0:                
                deltapos = self.param2                
            elif self.param1 == 2:
                deltapos = self.param1 - cp.position
            elif self.param1 == 40:
                deltapos = self.param1 - cp.position
            else:
                deltapos = (nfields - abs(self.param1 - cp.position))
                           
            cp.adv_pos(deltapos, nfields)
        elif self.type == 3:
            cp.balance = cp.balance + self.param1
                                
            
        