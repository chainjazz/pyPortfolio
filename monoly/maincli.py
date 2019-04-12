'''
Created on 24.12.2015.

@author: dkr85djo
'''
import struct
import socket
from MppyPlayer import MppyPlayer
from MppyPropertyInst import MppyPropertyInst
from MppyGame import MppyGame
from MppyField import MppyField
from MppyEvent import MppyEvent

def mppy_startcli():
    conn = socket.socket(type=socket.SOCK_DGRAM)
    #conn.connect(('127.0.0.1', 8088))
    print ("Contacting server...")
    conn.sendto(struct.pack("124s", b"Rastko"), ('127.0.0.1', 8088))
    me = MppyPlayer(25);
    
    while (me.id != 0):
        try:
            try:
                #print ("Waiting for server command...")                
                (b, a) = conn.recvfrom(128) #datagram receive/sends must
                                            # match in size, otherwise
                                            # OSError, msgsize wrong will be
                                            # raised; use unpack to split DGs
                                            # into variables       
                (c, s) = struct.unpack("!L124s", b)  # get cmd id
            
                # act according to cmd
            
                if c == 0x4:
                    print ("Syncing players...")
                    (n, s) = struct.unpack("!L120s", s)
                    print ("There are " + str(n) + " players...")
                    # TODO:...
                elif c == 0x0:                 
                    (m,) = struct.unpack("!124s", s) #single value is also a tuple
                    print("[Server] " + m.decode())
                elif c == 0x1:
                    print("Received player data")
                else:
                    pass
            except OSError as wtf:
                print (str(wtf.winerror))
        except KeyboardInterrupt:
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
    
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    

mppy_startcli()

