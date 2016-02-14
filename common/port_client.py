'''
Simple Client functionality
23 Dec 2014
Written by John Pecarina, Air Force Institute of Technology
john.pecarina@afit.edu
'''
import socket
import time

# class for a simple client that initiates a few kinds of connection modes
class Simple_Client:

    def __init__(self, host, port):
        self.my_svr_port = port     # tracks the port that this client's server is using
        self.my_svr_host = host     # tracks the host that tis client is on
        #Future config variables for init
        #self.broadcast_timeout = broadcast_timeout
        #self.broadcast_loops = broadcast_loops
        #self.connect_attempts = connect_attempts

    # Mode 1 - broadcast, to find peers in an unconfigured network
    def iterative_broadcast(self, host, min_port, random_offset, port_range, msg):
        # initialize the null reply
        reply = ""

        loops = 100
        while loops > 0: #should be a timeout
            loops = loops - 1
            # loop through all the ports (except my own)
            for p in range (0, port_range):
                # assign the port from the offset and loop around
                port = min_port + ((random_offset + p ) % port_range)
                # continue only if this is not my host and my port
                if not ((port == self.my_svr_port) & (host == self.my_svr_host)):
                    # calls the peer, if it is there
                    reply = self.attempt_to_connect(host, port, msg)
                # if it is there, we received a message that is not null
                if not (reply == ""):
                # just return it raw so the caller can handle format
                    return reply

        # if we got here, we got no connections, but let the caller handle it
        return reply

    
    #Mode 2 - attempt connection, can retry for # of attempts which is default to 1
    def attempt_to_connect(self, host, port, msg, attempts = 1):

        # Tracks successful sending and receiving
        isConnected = False
        connect_attempts = attempts # If you want to try multiple times, change this number
        reply = ""
        # The thread stays alive until successful sending and receiving
        while (not isConnected) & (connect_attempts >0):
            #print(connect_attempts),
            connect_attempts = connect_attempts - 1
            try:
                # blocking function that uses a socket to send and receive the message
                reply = self.connect_send__receive_close(host, port, msg)
                time.sleep(0.01)
                # if the send and receive function completed, we assume the message exchange occured
                isConnected = True # will enable exit of loop next time
                return reply
            # any errors are captured but not handled
            except:
                continue
        return reply
    
    
    #Mode 3 - connect_send__receive_close, basic functionality
    def connect_send__receive_close(self, host, port, msg):
        # Initialize the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        s.connect((host, port))
        # Send the reporting-in message
        s.send(msg.encode())
        # Receive the data in a buffer
        data = s.recv(8192)
        # If wou want to see the reply, uncomment these next two lines
        reply = data.decode('utf-8')
        #print("Client sent: " + msg + " to " + host + str(port) + ":" + reply)
        # Close the socket 
        s.close()
        return reply
