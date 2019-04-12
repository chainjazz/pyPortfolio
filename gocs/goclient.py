from Tkinter import * # --> CLIENT
from pickle import *
from socket import *

# NOTE
# TODO
# Combine server and client code into one module and
# use run-time logic to switch between the two
# The logic is not that much different

# CONSTANTS

dmn = 19 # This is supposed to be server-controlled
        # so variables depending on dmn and fds have to
        # be re-initialized *after* connecting to server
        # For now, we will fix the board to 19x19
fds = dmn * dmn
fra = 30 # stone radius in pixels, client-controlled

# GLOBALS


#TODO
# assuming clients have different ip's (for testing, use
#   local and dynamic-DNS host addresses) we can differentiate
#   players by ip, such that we compare the ip with the index
#   of the player (in this case, 2 players), and update corresponding
#   player's stats, filter-out illegal input, etc.

h = '192.168.1.100' # can be input via process args
p = 8088

canva = 0
canvas = 0
pr = 0 # guiding rectangle handle
il = 0 # infoline handle
cil = [0] * fds # board field handles
brd = [0] * fds # ze client baawd :)

def pinfo(t):
    canva.itemconfigure(il, text=t)

def UpdateBoardGui():
    for i in range(len(brd)):
        if brd[i] > 0:
            canvas.itemconfigure(cil[i], state="normal")
        else:
            canvas.itemconfigure(cil[i], state="hidden")
            
        if brd[i] == 1:
            canvas.itemconfigure(cil[i], fill="black")
        elif brd[i] == 2:
            canvas.itemconfigure(cil[i], fill="white")
            

def preCircle(event):
    global pr
    x = int(event.x / fra) * fra
    y = int(event.y / fra) * fra

    pinfo(str(event.x / fra) + "," + str(event.y / fra))

    if x >= 0 and x < fra * dmn and y >= 0 and y < fra * dmn:
        canvas.itemconfigure(pr,state="normal")
        canvas.coords(pr, (x, y, x+fra, y+fra))
    else:
        canvas.itemconfigure(pr, state="hidden")        

def decodeXY(ex, ey):
    xmod = ex % fra
    ymod = ey % fra
    x = int(ex / fra)
    y = int(ey / fra)    

    if xmod < fra and xmod > 0 and ymod < fra and ymod > 0:
        return y * dmn + x

def sendRequest(c):

    rsp = ""
        
    try:
        lesock.sendto(dumps(c), (h,p))
    except error, (s):
        pass #pinfo(s)

    while rsp == "":
        try:
            rsp = lesock.recvfrom(2048)
            return rsp
        except timeout, (v):
            #pinfo("Server down or net congestion")
            lesock.settimeout(0)
            return False
        except error, (s):
            #pinfo( s)
            return False

def requestPass(event):
    global brd      # server state vars

    cmn = 0         # init command var

    #pinfo("\n" + str(event.type))    
    cmn = ("PASS", 0)   # set command

    r = sendRequest(cmn)    # make request

    if r:
        brd = loads(r[0])   # process response
            
    UpdateBoardGui()        # refresh window

def requestPlace(event):
    global brd

    cmn = 0

    #pinfo(str(n) + "\n" + str(event.keycode))
    cmn = ("PLACE", decodeXY(event.x, event.y))

    r = sendRequest(cmn)

    if r:
        brd = loads(r[0])
    
    UpdateBoardGui()

def requestAdd():
    cmn = 0

    cmn = ("ADDPL", 0)

    r = sendRequest(cmn)

    UpdateBoardGui()
    
def connSrv():
    pass


# MAIN

if len(sys.argv) > 1:
    h = sys.argv[1]
    print "Trying " + str(h) + "..."    

try:
    lesock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    lesock.settimeout(1)
except error, (s):
    print s



root = Tk() # actual window, cannot be empty
canva = Canvas(root) # top-level "frame"
canvas = Canvas(canva) # board canvas
butt = Button(canva) # "connect to server" button

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
#root.geometry(str(dmn * fra + 256) + "x" + str(dmn * fra + 32) + "+128+128")
root.maxsize(dmn * fra + 256, dmn * fra + 32) # larger=non-resizable
#root.resizable(False, False)
canva.columnconfigure(0, weight=1)  # enables normal child positioning
canva.rowconfigure(0, weight=1)     # enables normal child positioning
canva.grid(column=0, row=0, sticky=(N, W, E, S))
canva.configure(bg="grey", width=str(dmn * fra + 256),
                height=str(dmn * fra + 32))
canvas.grid(column=0, row=0, sticky=(W))
canvas.configure(bd="1", relief="raised") #border
canvas.configure(width=str((dmn * fra) + 4), height=str((dmn*fra) + 4), bg="yellow")
canvas.xview_moveto(.05)    # do we need canvasx mouse-event correction?
canvas.yview_moveto(.05)    # do we need canvasx mouse-event correction?
butt.configure(command=connSrv, height="1", width="24", text="Connect")
il = canva.create_text((19 * 30 + 128, 30))
bc = canva.create_window((19 * 30 + 128, 255), window=butt)
pr = canvas.create_rectangle((0, 0, 30, 30), state="hidden")
    
for i in range(len(brd)): # board field creation
    cil[i] = canvas.create_oval((i % dmn * fra,
                                i / dmn * fra,
                                i % dmn * fra + fra,
                                i / dmn * fra + fra),
                                state="hidden")

canva.itemconfigure(il, fill="blue", width="128") #stylize status bar
canvas.bind("<Motion>", preCircle)
canvas.bind("<1>", requestPlace) # weird event naming convention; check TkDocs
canvas.bind("<2>", requestPass)

UpdateBoardGui()
requestAdd()

# START OF GUI CODE

root.mainloop()

# END OF GUI CODE

try:
    lesock.close()
except error, (s):
    print s
    

