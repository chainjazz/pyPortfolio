'''
Created on 22.12.2015.

@author: dkr85djo
'''

class MppyProperty(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.price = 0
        self.revenue = [0, 0, 0, 0, 0, 0, 0] # indexed by devlevel, multiplied by grplevel
        self.colourgroup = 0 # id of colourgroup
        self.maxdevlevel = 0 # max development level for certain property types
        self.maxgrplevel = 0 # max group level (1 = binary, 2-4 for stations, etc.)
        self.name = "Property" + str(id)