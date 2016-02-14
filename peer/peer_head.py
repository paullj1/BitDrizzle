<<<<<<< HEAD
'''
Written by John Pecarina, Air Force Institute of Technology,
john.pecarina@afit.edu
Modified by _______________, Date: 
'''
import logging
import socket
import threading
import time

from common.data_store import Data
from peer.local_listener import Simple_Listener
from peer.net_node import NetNode
from peer.net_server import Simple_Server
from peer.router import Router


class PeerHead:

    def __init__(self, host, port, peer_sock, local_sock, start_port, port_range):
        self.node = NetNode(host, port)
        self.router = Router(self.node)
        self.data = Data()
        self.peer_server = Simple_Server(peer_sock, self)
        self.local_listener = Simple_Listener(local_sock, self)
        self.start_port = start_port
        self.port_range = port_range

    def start_peer_server(self):
        self.peer_server.serve()

    def start_local_listener(self):
        self.local_listener.serve()

    def findPeer(self, host):
        #the function below finds the host we contacted
        r_node = self.router.find_peer(host, self.start_port, self.port_range)
        #The remote host and remote port will be set as the DHT entry point for this node
        self.router.setEntry(r_node)
        return r_node.toString()

    def joinNetwork(self):
        #LOOKUP OF THIS NODE:#####################################################
        #If the Router gave us a peer, then we can lookup in the network
        #First call lookup( ) to get the location where we belong in the network (succ(my_id))
        #Lookup of hashed_ID will give us the succ
        succ = self.router.lookup(self.node.hash, self.router.getEntry())
        #print ("Did lookup! Host: " + succ.host + " at  Port: " + str(succ.port) + " Hash: " + succ.hash)

        #INSERT NODE#############################################################
        #Insert sets pred, succ after coordination in the network
        pred = self.router.insert(self.node.hash, succ)
        #print ("Did insert! Host: " + pred.host + " at  Port: " + str(pred.port) + " Hash: " + pred.hash)

        # We can set pred and succ now, probably could add error checks (for null) and a loop to retry
        self.router.setPred(pred)
        # they should also be set at the same time so they are consistent in the network
        self.router.setSucc(succ)
        # the successor should default to succ as well
        self.router.setEntry(succ)
        return ("Joined at: " + succ.toString())

    def getFullNetStatus(self):
        return ("######### Node " + str(self.router.port) + " Routing Information########|\n" +
                "SELF:" + self.node.hash + "|" + self.node.host + "|" + str(self.node.port) + "|\n"
                "PRED:" + self.router.getPred().hash + "|" + self.router.getPred().host + "|" + str(self.router.getPred().port)+ "|\n"
                "SUCC:" + self.router.getSucc().hash + "|" + self.router.getSucc().host + "|" + str(self.router.getSucc().port)+ "|\n"  )

    def getCSVNetStatus(self):
        return(str(self.router.port) + "," + self.node.hash + "," + self.node.host + "," + str(self.node.port) +    #this node info
            "," + self.router.getPred().hash + "," + self.router.getPred().host + "," + str(self.router.getPred().port) +  #pred node
            "," + self.router.getSucc().hash + "," + self.router.getSucc().host + "," + str(self.router.getSucc().port) )     #succ node


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

class Drizzler(threading.Thread):

    '''
    Initialization/Constructor
    '''
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        self.host = self.args[0]
        self.peer_port = int(self.args[1])
        self.local_port = int(self.args[2])
        self.start_port = int(self.args[3])
        self.port_range = int(self.args[4])
        self.multi_mode = int(self.args[5])

        self.peer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.local_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try to bind to all given ports
        self.peer_sock.bind((self.host, self.peer_port))
        self.local_sock.bind((self.host, self.local_port))
        self.peer_head = None

    def run(self):
        logging.debug('running with %s', self.args)

        self.peer_head = PeerHead(self.host, self.peer_port, self.peer_sock, self.local_sock, self.start_port, self.port_range)

        self.peer_head.start_peer_server()

        self.peer_head.start_local_listener()

        if not self.multi_mode == 0:
            self.peer_head.findPeer(self.host)
            self.peer_head.joinNetwork()

        while True:
           time.sleep(10)
=======
'''
Written by John Pecarina, Air Force Institute of Technology,
john.pecarina@afit.edu
Modified by _______________, Date: 
'''
import logging
import socket
import threading
import time

from common.data_store import Data
from peer.local_listener import Simple_Listener
from peer.net_node import NetNode
from peer.net_server import Simple_Server
from peer.router import Router


class PeerHead:

    def __init__(self, host, port, peer_sock, local_sock, start_port, port_range):
        self.node = NetNode(host, port)
        self.router = Router(self.node)
        self.data = Data()
        self.peer_server = Simple_Server(peer_sock, self)
        self.local_listener = Simple_Listener(local_sock, self)
        self.start_port = start_port
        self.port_range = port_range

    def start_peer_server(self):
        self.peer_server.serve()

    def start_local_listener(self):
        self.local_listener.serve()

    def findPeer(self, host):
        #the function below finds the host we contacted
        r_node = self.router.find_peer(host, self.start_port, self.port_range)
        #The remote host and remote port will be set as the DHT entry point for this node
        self.router.setEntry(r_node)
        return str(r_node)

    def joinNetwork(self):
        #LOOKUP OF THIS NODE:#####################################################
        #If the Router gave us a peer, then we can lookup in the network
        #First call lookup( ) to get the location where we belong in the network (succ(my_id))
        #Lookup of hashed_ID will give us the succ
        succ = self.router.lookup(self.node.hash, self.router.getEntry())
        #print ("Did lookup! Host: " + succ.host + " at  Port: " + str(succ.port) + " Hash: " + succ.hash)

        #INSERT NODE#############################################################
        #Insert sets pred, succ after coordination in the network
        pred = self.router.insert(self.node.hash, succ)
        #print ("Did insert! Host: " + pred.host + " at  Port: " + str(pred.port) + " Hash: " + pred.hash)

        # We can set pred and succ now, probably could add error checks (for null) and a loop to retry
        self.router.setPred(pred)
        # they should also be set at the same time so they are consistent in the network
        self.router.setSucc(succ)
        # the successor should default to succ as well
        self.router.setEntry(succ)
        return "Joined at: {}".format(str(succ))

    def getFullNetStatus(self):
        return ("######### Node " + str(self.router.port) + " Routing Information########|\n" +
                "SELF:" + self.node.hash + "|" + self.node.host + "|" + str(self.node.port) + "|\n"
                "PRED:" + self.router.getPred().hash + "|" + self.router.getPred().host + "|" + str(self.router.getPred().port)+ "|\n"
                "SUCC:" + self.router.getSucc().hash + "|" + self.router.getSucc().host + "|" + str(self.router.getSucc().port)+ "|\n"  )

    def getCSVNetStatus(self):
        return(str(self.router.port) + "," + self.node.hash + "," + self.node.host + "," + str(self.node.port) +    #this node info
            "," + self.router.getPred().hash + "," + self.router.getPred().host + "," + str(self.router.getPred().port) +  #pred node
            "," + self.router.getSucc().hash + "," + self.router.getSucc().host + "," + str(self.router.getSucc().port) )     #succ node


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

class Drizzler(threading.Thread):

    '''
    Initialization/Constructor
    '''
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        self.host = self.args[0]
        self.peer_port = int(self.args[1])
        self.local_port = int(self.args[2])
        self.start_port = int(self.args[3])
        self.port_range = int(self.args[4])
        self.multi_mode = int(self.args[5])

        self.peer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.local_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try to bind to all given ports
        self.peer_sock.bind((self.host, self.peer_port))
        self.local_sock.bind((self.host, self.local_port))
        self.peer_head = None

    def run(self):
        logging.debug('running with %s', self.args)

        self.peer_head = PeerHead(self.host, self.peer_port, self.peer_sock, self.local_sock, self.start_port, self.port_range)

        self.peer_head.start_peer_server()

        self.peer_head.start_local_listener()

        if not self.multi_mode == 0:
            self.peer_head.findPeer(self.host)
            self.peer_head.joinNetwork()

        while True:
           time.sleep(10)
>>>>>>> 0cefe66fce0f99a1a0af9321a575243e82b4a242
