'''
LocalHead -
Supports data operation of writing to a local key value store
Also supports user communication to the peer head through socket communication

Written by John Pecarina, Air Force Institute of Technology,
john.pecarina@afit.edu
Feb 1 2016
Modified by _______________, Date:
'''
from common.data_store import Data, DataItem
from common.port_client import Simple_Client

class LocalHead:

    # initiate the class with the host and port of the listener
    def __init__(self, host, port):
        #also init the app_support data hash table
        self.data = Data()
        self.host = host
        self.port = port
        return

    # function checks if port is receiving messages, which happens after peer is networked to the DHT
    def hasListener(self):
        response = ""
        client = Simple_Client(self.host, self.port)
        try:
            response = client.connect_send__receive_close(self.host, self.port, "PING|")
        except:
            return False
        if response == "OK":
            return True
        return False

	# ask the peer_head if this node is in the network
    def getNeighbors(self, mode):
        # we need a client to talk to the peer head
        client = Simple_Client(self.host, self.port)
        if mode == "FULL":
            msg = "GET_NET_STAT|FULL"
        else:
            msg = "GET_NET_STAT|CSV"

        # send the data and return
        response = client.connect_send__receive_close(self.host, self.port, msg)
        return response

	# ask the peer_head to find a network entry node
    def findPeer(self):
        # we need a client to talk to the peer head
        client = Simple_Client(self.host, self.port)
        msg = "FIND_PEER|" + self.host
        # send the data and return
        response = client.connect_send__receive_close(self.host, self.port, msg)
        return response

	# ask the peer_head to find a network entry node
    def locateHash(self, hash):
        # we need a client to talk to the peer head
        client = Simple_Client(self.host, self.port)
        msg = "LOOKUP|" + hash
        # send the data and return
        response = client.connect_send__receive_close(self.host, self.port, msg)
        return response

	# ask the peer_head to find a network entry node
    def joinNetwork(self):
        # we need a client to talk to the peer head
        client = Simple_Client(self.host, self.port)
        msg = "JOIN_NETWORK|"
        # send the data and return
        response = client.connect_send__receive_close(self.host, self.port, msg)
        return response

    # function writes to the app_support store
    def writeLocal(self, value):
        # make this a data item
        d_item = DataItem(value)
        # write it into the app_support store
        self.data.write(d_item.key, d_item.value)
        return d_item.key

	# function writes to the network
    def writeToNet(self, value):
        # we need a client to talk to the peer head
        client = Simple_Client(self.host, self.port)
        # put a header so the app_support server knows what to do with the data string
        d_item = DataItem(value)
        msg = "WRITE_DATA|" + d_item.key + "|" + d_item.value
        # send the data and return
        client.connect_send__receive_close(self.host, self.port, msg)
        return d_item.key

    def deleteFromNet(self, key):
        # we need a client to talk to the peer head
        client = Simple_Client(self.host, self.port)
        # put a header so the app_support server knows what to do with the data string
        msg = "DELETE|" + key
        # send the data and return
        return client.connect_send__receive_close(self.host, self.port, msg)

    def readFromNet(self, key):
        # we need a client to talk to the peer head
        client = Simple_Client(self.host, self.port)
        # put a header so the app_support server knows what to do with the data string
        msg = "READ|" + key
        # send the data and return
        return client.connect_send__receive_close(self.host, self.port, msg)

	#Implement these functions
	#def readLocal(self, key):
	#def deleteLocal(self, key):

    #for printing the data
    def DumpLocalData(self):
        return self.data.toString()

    #for printing the data
    def DumpPeerData(self):
        # we need a client to talk to the peer head
        client = Simple_Client(self.host, self.port)
        msg = "DUMP_PEER_DATA|"
        # send the data and return
        response = client.connect_send__receive_close(self.host, self.port, msg)
        return response
