'''
Simple Single Threaded Server
23 Dec 2014
Written by John Pecarina, Air Force Institute of Technology,
john.pecarina@afit.edu
Modified by _______________, Date: 

This program defines the simple server class variable and calls the server into
operation.

The server simulates an action with a fixed service time. The fixed
service time is an experimental variable: service_time. Other key variables are
the socket address which this service binds to.

Program execution follows a single thread for every client-server session. The
server receives a simple text message from the client, performs an action and
replies with a simple text response. Upon receipt of the end message ('bye'),
the server shuts itself down.
'''
import logging
import threading

from common.port_client import Simple_Client
from peer.net_node import NetNode

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


class Simple_Server():

    '''
    Initialization/Constructor
    '''
    def __init__(self, sock, peer_head):
        self.sock = sock
        self.head = peer_head
        self.host = self.head.router.host
        self.port = self.head.router.port

    def serve(self):
        # opens the socket for messages        
        self.sock.listen(2)
        #logging.debug('Waiting for peer connections')
        # calls the function that accepts connections
        t = threading.Thread(target=self.acceptConnections)
        t.start()
        return

    '''
    Function definition accepts and handles incoming connections in a single threaded fashion
    '''
    def acceptConnections(self):
       
        while (True):
            ''' accept a connection and call the respond method... '''
            try:
                conn, addr = self.sock.accept()   #Accepts the connection on the socket determined above
                #print ('Server Connected to: '+addr[0]+ ' : '+str(addr[1])) #Prints the connection information of the client
                self.respond(conn)                              #jumps to respond function
            except:
                continue
        return


    '''
    Function to handle the server response to the client
    '''
    def respond(self, conn):

        msg = ''
        data = conn.recv(8192)                  # stores information received from the socket as the variable data

        msg = data.decode('utf-8')
        #print("Server received: " + msg )
        
        reply = self.performAction(msg)
        
        #print(" ...sending: " + reply)

        conn.sendall(reply.encode())                     # sends the reply over the socket.


    '''
    Server simulates the doing of an action with a fixed service time. Feel free to alter this
    function by adding a service time based on a random distribution for extra credit.
    '''
    def performAction(self, msg):
        m = msg.split('|')

        if (m[0] == "FIND_PEER"):
            #return this nodes info, easily done
            return self.host + ":" + str(self.port)
        
        if (m[0] == "LOOKUP"):
            #lookup()
            code = m[1]         #hash_code being sent as a lookup
            host = m[2]         #host of the requester
            port = int(m[3])    #port of the requester

            mine = self.head.node.hash  #my hashed ID
            succ = self.head.router.succ.hash # my succ's hashed ID
            pred = self.head.router.pred.hash # my pred's hashed ID

            # 4 ways that the lookup returns my node (SELF RESPONSES INDICATE Completion)
            # 1: if pred = mine = succ: (one node network)
            if (pred == mine) & (mine == succ):
                #send succ(hash_code) = mine ID back to client
                return (mine + ":" + self.host + ":" + str(self.port))
            # 2: if pred < hash_code & hash_code <= self & pred < self:
            # (no boundary check, if my node is the last, but not the first)
            if (pred < code) & (code <= mine) & (pred  < mine):
                #send succ(hash_code) = mine ID back to client
                return (mine + ":" + self.host + ":" + str(self.port))
            # 3: if pred < hash_code & hash_code > self & pred > self:
            # (pred is last node before flip, id first after, hash is before the flip)
            if (pred < code) & (code > mine) & (pred  > mine):
                #send succ(hash_code) = mine ID back to client
                return (mine + ":" + self.host + ":" + str(self.port))         
            # 4: if pred > hash_code & hash_code <= self & pred > self:
            # (pred is last node before flip, id first after, hash is after the flip)
            if (pred > code) & (code <= mine) & (pred  > mine):
                #send succ(hash_code) = mine ID back to client
                return (mine + ":" + self.host + ":" + str(self.port)) 

            # ALL OTHER CASES Return the successor (which implicitly indicates non completion)
            # Alternate implementations could have server call lookup on successor (recursive)
            # But this implementation returns the succ for the client to do next lookup (iterative)
            
            return (succ + ":" + self.head.router.succ.host +
                            ":" + str(self.head.router.succ.port))
            
        
        if (m[0] == "INSERT"):
            #insert()
            code = m[1]  #hash_code being sent in insert
            host = m[2]   #host of the requester
            port = int(m[3])  #port of the requester
            # we need to save the old pred info in case we overwrite the object
            old_pred_code = self.head.router.pred.hash
            old_pred_host = self.head.router.pred.host
            old_pred_port = self.head.router.pred.port
            #creating the new predecessor object from the message
            new_pred = NetNode(host, port)

            #if this is a new network, set all to the new node, return self info
            if ((old_pred_code == self.head.node.hash) &
                (self.head.router.succ.hash == self.head.node.hash)):
                self.head.router.setPred(new_pred)
                self.head.router.setSucc(new_pred)
                self.head.router.setEntry(new_pred)
                return (old_pred_code + ":" + old_pred_host + ":" + str(old_pred_port))
            
            #INSERT is the 1st of 3 messages, the 2nd is sent to the pred
            # we need a temp client for that
            temp_client = Simple_Client(self.host, self.port)
            # craft a message for the old_pred server to update its successor to the new pred
            msg = "UPDATE_SUCC" + "|" + code + "|" + host + "|" + str(port)
			
            # connect to the current predecessor to update pointer to succ            
            response = temp_client.attempt_to_connect(old_pred_host, old_pred_port, msg)
            # if the response was "UPDATED_SUCC_OK" then we set the new_pred and return the old one
            if(response == "UPDATED_SUCC_OK"):
                # update the new predecessor
                self.head.router.setPred(new_pred)
                # return info on the old predecessor
                return (old_pred_code + ":" + old_pred_host + ":" + str(old_pred_port))
            #else:
            return ""
        
        if (m[0] == "UPDATE_SUCC"):
            #update_succ()
            code = m[1]  #hash_code being sent in update_succ is that of the new succ
            host = m[2]   #host of the new succ
            port = int(m[3])  #port of the new succ 
            #creating the new successor object from the message
            new_succ = NetNode(host, port)
            #updating the app_support node
            self.head.router.setSucc(new_succ)
            #no error checking yet
            return "UPDATED_SUCC_OK"
                        
        if (m[0] == "WRITE_DATA"):
            #write()
            key = m[1]  #hash_code being sent in write
            value = m[2]
            host = m[3]   #host of the requester
            port = int(m[4])  #port of the requester

            self.head.data.write(key, value)
            return "OK"
			
		#Implement these handlers 			
        if (m[0] == "READ_DATA"):
            key = m[1]
            print("Trying to read key: {0}".format(key))
            print("My info: {0}:{1}".format(self.host, self.port))
            return self.head.data.read(key)

        #not using this, just write("0")
        if (m[0] == "DELETE_DATA"):
            return self.host + str(self.port) + " Reading Data..."

        return "CMD NOT FOUND"
