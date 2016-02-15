'''
Simple Single Threaded Server
23 Dec 2014
Written by John Pecarina, Air Force Institute of Technology,
john.pecarina@afit.edu

Modified by Colin Busho, Kevin Cooper, Paul Jordan, and Chip Van Patten
Last Modified:  14 Feb 2016

This program defines the simple server class variable and calls the server into
operation.

'''
import threading


class Simple_Listener():

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
        #logging.debug('Waiting for app_support connections')
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
                #Debug the connection information of the client
                #logging.debug('Local Server at %s Connected to: %s at %s', self.port, addr[0], str(addr[1]))
                self.respond(conn)                              #jumps to respond function
            except:
                continue


    '''
    Function to handle the server response to the client
    '''
    def respond(self, conn):

        msg = ''
        data = conn.recv(2048)                  # stores information received from the socket as the variable data
        msg = data.decode('utf-8')
        #logging.debug('Message at Local server: %s', msg)
        reply = self.performAction(msg)
        conn.sendall(reply.encode())                     # sends the reply over the socket.


    '''
    Server simulates the doing of an action with a fixed service time. Feel free to alter this
    function by adding a service time based on a random distribution for extra credit.
    '''
    def performAction(self, msg):

        m = msg.split('|')

        if (m[0] == "GET_NET_STAT"):
            if m[1] == "FULL":
                return self.head.getFullNetStatus()
            else:
                return self.head.getCSVNetStatus()

        if (m[0] == "FIND_PEER"):
            if (len(m) < 2):
                return "NEED TARGET HOST"
            target_host = m[1]
            return self.head.findPeer(target_host)

        if (m[0] == "LOOKUP"):
            if (len(m) < 2):
                return "NEED HASH CODE"
            hash_code = m[1]
            return str(self.head.router.lookup(hash_code, self.head.router.getEntry()))

        if (m[0] == "JOIN_NETWORK"):
            return self.head.joinNetwork()

        if (m[0] == "WRITE_DATA"):
            key = m[1]         #hash_code being sent as a lookup
            value = m[2]         #host of the requester
            data_succ = self.head.router.lookup(key, self.head.router.succ)
            #logging.debug(data_succ.hash)
            self.head.router.write(key, value, data_succ)
            return "OK"

        if (m[0] == "READ_DATA"):
            if (len(m) < 4):
                return "NEED HASH CODE & TARGET HOST"
            hash_code = m[1]
            host = m[2]
            port = m[3]
            print("Hash code received at local_listener {0}".format(hash_code))
            print("My info {0}:{1}".format(self.host, self.port))
            print("Destination {0}:{1}".format(host, port))

            return str(self.head.router.read(hash_code, self.head.router.getEntry()))

        if (m[0] == "DELETE"):
            if (len(m) < 2):
                return "NEED HASH CODE"
            hash_code = m[1]
            data_succ = self.head.router.lookup(hash_code, self.head.router.succ)
            if (self.head.router.write(hash_code, "0", data_succ)):
                return "Deleted: {0} from {1}".format(hash_code, str(data_succ))
            return "DELETE FAILED!"

        if (m[0] == "DUMP_PEER_DATA"):
            return str(self.head.data)

        if (m[0] == "PING"):
            return "OK"

        return "CMD NOT FOUND"
