
# -*- coding: utf-8 -*-

#####################################################################
# GO.PY - Program/library implementation of simple rule logic of GO
#
# Napisao Rastko Petrovic
#
#####################################################################

###########
# PREPROC #
###########

import random

#############
# CONSTANTS #
#############

dmn = 19
fds = dmn * dmn

###########
# GLOBALS #'
###########

# initialize board
brd = [0] * fds # main board

# validation helpers
cbd = [0] * fds # floodfill mask board
lbd = [0] * fds # liberty debug board
gsc = 0 # group stone count
lic = 0 # stone liberty count


###############
# DEFINITIONS #
###############

# ALGO for checking validity of move
#
#   Basically, you don't check validity.
#   You check the liberties twice, before and after
#   incrementing the turn counter; if only this player's liberties checkout before,
#   check for KO; if KO checks out, increment; if they
#   don't checkout, reset to previous, and wait for another input
#   then check all liberties (or just the other player's?) and update board

# ALGO for checking board
#
#   Check next field/junction
#       If not empty, set color for check
#           (Floodfill check, should be separate for comprehension)
#
#               If same color, set check flag, add group count and recurse
#               If empty, add liberty count (but not global check flag)
#               If different color skip
#
#           Check liberty and group count
#           
# 

# Check board and remove captured stones
def CheckBoard():
    
    global brd, cbd, gsc, lic

    cbd = [0] * fds # possibly not needed...
    i = 0

    for x in range(len(brd)):
        if CheckStone(x) > 0:
            pass # returns number of captured stones
        else:
            i += RemoveCaptured()

    return i # return number of captured stones


# Check single stone
def CheckStone(i):
    global cbd, lbd, gsc, lic

    cbd = [0] * fds     # floodfill check reset
                        #
                        # NOTE: even though this makes
                        # the loop go through all fields
                        # regardless of what's been checked (optimization issue),
                        # group liberties are shared and need to be flagged,
                        # and subsequent iterations need to recount these
                        # liberties (algorithm issue)
    gsc = 0             # group counter reset
    lic = 0             # liberty counter reset 

    if brd[i] != 0:     # if field NOT empty
        CheckLiberty(i, brd[i])
        lbd[i] = lic    # debug
        return lic
    else:
        lbd[i] = 0
        return 1


# Check stone liberties, recursive floodfill group tracing style
def CheckLiberty(i, a):

    global cbd, gsc, lic

    # default neighbours definition (4-way floodfill)
    naboer = [i - dmn, i + 1, i + dmn, i - 1]

    # no need for stop conditions to be ELSEd, because they break
    # the function
    if cbd[i] == a:         # original floodfill stop condition
                            #   ("replacement-color", but basically
                            #   a bit-mask is used here, value could
                            #   be anything)
        #print "=",
        return    

    if brd[i] == 0:         # if empty       
        lic += 1            # increment liberty count
        cbd[i] = a          # flag as checked (in THIS group trace)
        #print "L",
        return    

    if brd[i] != a:       # neither empty nor floodfill checked;
                            # therefore, oponnents' piece
        #print "x",
        return

    # set neighbour definition based on
    # special positions on the board, otherwise
    # use default definition above (implied else)
    if i == 0:                              # TL corner           
        naboer = [i + 1, i + dmn]
    elif i == dmn - 1:                      # TR corner
        naboer = [i - 1, i + dmn]
    elif i == (dmn - 1) * dmn:              # BL corner
        naboer = [i + 1, i - dmn]
    elif i == fds - 1:                      # BR corner
        naboer = [i - 1, i - dmn]
    elif i < dmn:                           # on the top line
        naboer = [i + 1, i + dmn, i - 1]
    elif i >= (dmn - 1) * dmn:              # on the bottom line
        naboer = [i - dmn, i + 1, i - 1]
    elif i % dmn == 0:                      # on the left line
        naboer = [i - dmn, i + 1, i + dmn]
    elif i % dmn == dmn - 1:                # on the right line
        naboer = [i - dmn, i + dmn, i - 1]

    # All that follows happens only once for each field,
    #   or recursively only if tracing a group
    
    cbd[i] = a  # set floodfill "replacement color"
                # (checkflag, bitmask, etc.)
    #print ".", 

    for k in range(len(naboer)):            # for each neighbour
        CheckLiberty(naboer[k], brd[i])        
        
    gsc += 1 # increment group stone counter; happens
            #   only if tracing group (based on ifelse order)

# encapsulation of captured stone removal procedure
#   (called it procedure, since it takes no local args,
#   therefore depends on correct placement in the caller)
def RemoveCaptured():
    global brd

    i = 0

    # basically, sets all checked fields to empty
    # works b/c empty fields are checked, but empty anyways,
    # and opponent stones are not checked
    for x in range(len(brd)):
        if cbd[x] == brd[x]:
            brd[x] = 0
            i += 1

    return i

# randomly fill board for debugging
def RandomBoard():
    
    random.seed(20)

    for j in range(len(brd)):
        brd[j] = random.randint(0, 2)

    


        
        
