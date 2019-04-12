'''
Created on 24.12.2015.

@author: dkr85djo
'''

class MppyField(object):
    '''
    classdocs
    '''


    def __init__(self, i):
        '''
        Constructor
        '''
        self.type = 0 # 1 = property
                        # 2 = event (chance + chest combo)
                        # 3 = jail
                        # 4 = freeparking
                        # 5 = gotojail
                        # 6 = tax
                        # 7 = start
        self.propertyid = 0 # id of property
        self.id = i # id of field, start from 1        