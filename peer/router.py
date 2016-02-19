'''
Written by John Pecarina, Air Force Institute of Technology,
john.pecarina@afit.edu
Modified by _______________, Date:
'''

from common.port_client import Simple_Client
from peer.net_node import NetNode

#the router class provides basic DHT functionality, routing is simple, pred and succ only
class Router:

    # init builds the router
    def __init__(self, self_node):
        self.pred = self_node   #these should eventually be replaced by a routing table
        self.succ = self_node   #pred is the previous node, succ is the next one after me
        self.host = self_node.host  #the IP of the host server
        self.port = self_node.port  #the port of the host server
        self.entry = None   # entry node into the P2P network, set after find_peer

    '''
    GETTERS AND SETTERS
    '''
    def getPred(self):
        return self.pred

    def getSucc(self):
        return self.succ

    def setPred(self, pred):
        self.pred = pred

    def setSucc(self, succ):
        self.succ = succ

    def setEntry(self, entry):
        self.entry = entry

    def getEntry(self):
        return self.entry

    #find peer looks for an initial node to route through
    def find_peer(self, target_host, min_port, port_range):
        # the concept is to start at a random port, loop around until we get to a host that will respond
        max_port = min_port + port_range      # find the max range
        random_offset = 0 # = random.randint(min_port, self.port) # choose a random port in range
        # create a client for this operation
        client = Simple_Client(self.host, self.port)

        # instruct the client to 'broadcast' and loop through all peer addresses
        response = client.iterative_broadcast(target_host, min_port, random_offset, port_range, "FIND_PEER")
        if response == "":
            return (NetNode("None",0))
        # the response should be a tuple, separated by ':', but there is no type checking, sorry
        r_host, r_port = response.split(':')
        # we create a remote node for this
        r_node = NetNode(r_host, (int(r_port)))
        # then we stop and return the remote node
        return r_node

    # iterative version of lookup, where this client continues lookup until the succ() node of the hash is found
    # in other words, we do the work of the lookup, not the server we contact
    # the starting node of the lookup is net_node, which is an initial entry node, or our node's succ()
    def lookup(self, hash_code, net_node):
        # create a client for this operation
        client = Simple_Client(self.host, self.port)
        # the lookup request is always the same
        msg = "LOOKUP|{0}|{1}|{2}".format(hash_code, self.host, self.port)

        succ_node = NetNode("None", 0)

        # since this implementation of lookup is iterative, so we need to keep track of the nodes we've queried
        # the last hash inits as the code we are looking for, but is updated as the last node we checked
        last_hash = hash_code
        # our successor's hash inits as the entry node of the lookup
        succ_hash = net_node.hash
        succ_host = net_node.host
        succ_port = net_node.port
        # if the pred and succ hashes ever are equal, it means that the node we are going to check next
        # is the same node as the one we just checked, which means we are done searching
        while not (last_hash == succ_hash):
            # the server at succ is contacted, response is the succ node to the hash
            response = client.attempt_to_connect(succ_host, succ_port, msg)
            #print ("Lookup:" + response)
            # since we just checked succ, we can copy that info to last_hash
            last_hash = succ_hash
            # the response should be a few strings, separated by ':', but there is no type checking, sorry
            if not response == "":
                # the response contained the next node to check, so it is assigned to the current successor
                succ_hash, succ_host, succ_port_str = response.split(':')
                # succ_port_str was sent as a string and now is converted to an int
                succ_port = int(succ_port_str)
            else:
                return("NO LOOKUP RESPONSE ERROR!")

        # we create a remote node for this succ
        succ_node = NetNode(succ_host, (int(succ_port)))
        # the server returned self or its succ, if it returned self, then we will exit the loop and return
        return succ_node

    def insert(self, hash_code, succ_node):
        # create a client for this operation
        client = Simple_Client(self.host, self.port)
        # the insert request is like lookup
        msg = "INSERT|{0}|{1}|{2}".format(hash_code, self.host, self.port)

        # the server at succ is contacted, response is the pred node of our node
        response = client.attempt_to_connect(succ_node.host, succ_node.port, msg)
        # the server returned the predecessor
        if response == "":
            print("NO INSERT RESPONSE ERROR!")
            exit(0)
        # the response should be a string of strings, separated by ':', but there is no type checking, sorry
        # the response contained the pred node after the coord in the network was complete
        pred_hash, pred_host, pred_port_str = response.split(':')
        # pred_port_str was sent as a string and now is converted to an int
        pred_port = int(pred_port_str)
        # we create a remote node for this pred
        pred_node = NetNode(pred_host, (int(pred_port)))
        # then we stop and return the remote node
        return pred_node

    def leave(self, pred_node, succ_node):
        ### First update successor of our predecessor
        # create a client for this operation
        client = Simple_Client(self.host, self.port)
        # the insert request is like lookup
        msg = "UPDATE_SUCC|{0}|{1}|{2}".format(succ_node.hash, succ_node.host, succ_node.port)
        # the server at succ is contacted, response is the pred node of our node
        response = client.attempt_to_connect(pred_node.host, pred_node.port, msg)
        # the server returned the predecessor
        if response == "":
            print("NO INSERT RESPONSE ERROR!")
            exit(0)

        ### Next, update predecessor of our successor
        msg = "UPDATE_PRED|{0}|{1}|{2}".format(pred_node.hash, pred_node.host, pred_node.port)
        # the server at succ is contacted, response is the pred node of our node
        response = client.attempt_to_connect(succ_node.host, succ_node.port, msg)
        # the server returned the successor
        if response == "":
            print("NO INSERT RESPONSE ERROR!")
            exit(0)

        # Okay
        return "OK"

    def write(self, key, value, succ_node):
        # create a client for this operation
        client = Simple_Client(self.host, self.port)
        # the insert request is like lookup
        msg = "WRITE_DATA|{0}|{1}|{2}|{3}".format(key, value, self.host, self.port)

        # the server at succ is contacted, response is the okay
        response = client.attempt_to_connect(succ_node.host, succ_node.port, msg)
        # the server returned the predecessor
        if response == "":
            return ("NO READ RESPONSE ERROR!")
        if response == "OK":
            return True
        return False

    def read(self, key, succ_node):
        # create a client for this operation
        client = Simple_Client(self.host, self.port)
        # the insert request is like lookup
        msg = "READ_DATA|{0}|{1}|{2}".format(key, self.host, self.port)

        # the server at succ is contacted, response is the okay
        response = client.attempt_to_connect(succ_node.host, succ_node.port, msg)
        # the server returned the predecessor
        if response == "":
            return ("NO READ RESPONSE ERROR!")
        if response == " ":
            return None
        return response

    def getNetSize(self, hash_code):
        # create a client for this operation
        client = Simple_Client(self.host, self.port)
        # the lookup request is always the same
        msg = "LOOKUP|{0}|{1}|{2}".format(hash_code, self.host, self.port)

        succ_node = NetNode("None", 0)

        # since this implementation of lookup is iterative, so we need to keep track of the nodes we've queried
        # the last hash inits as the code we are looking for, but is updated as the last node we checked
        last_hash = hash_code
        # our successor's hash inits as the entry node of the lookup
        succ_hash = self.succ.hash
        succ_host = self.succ.host
        succ_port = self.succ.port
        # if the pred and succ hashes ever are equal, it means that the node we are going to check next
        # is the same node as the one we just checked, which means we are done searching
        count = 1 # to account for first node
        while not (last_hash == succ_hash):
            count = count + 1
        
            # the server at succ is contacted, response is the succ node to the hash
            response = client.attempt_to_connect(succ_host, succ_port, msg)
            # since we just checked succ, we can copy that info to last_hash
            last_hash = succ_hash
            # the response should be a few strings, separated by ':', but there is no type checking, sorry
            if not response == "":
                # the response contained the next node to check, so it is assigned to the current successor
                succ_hash, succ_host, succ_port_str = response.split(':')
                # succ_port_str was sent as a string and now is converted to an int
                succ_port = int(succ_port_str)
            else:
                return("NO LOOKUP RESPONSE ERROR!")

        # the server returned self or its succ, if it returned self, then we will exit the loop and return
        return "Total nodes in network: {0}".format(count)
