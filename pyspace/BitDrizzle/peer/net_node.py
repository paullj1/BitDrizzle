import hashlib

# class definition for a network node, which contains addressing at a minimum
class NetNode:

    def __init__(self, host, port):
        self.host = host    #host address of remote machine
        self.port = port    #port of remote machine
        self.hash = self.getHashedID()  # a hash ID for the node

    # implements MD5 hash over the string that describes the host and port of the remote node
    def getHashedID(self):
        id_string = self.host + str(self.port)
        return hashlib.md5(id_string.encode('utf-8')).hexdigest().upper()

    def toString(self):
        return self.host + "," + str(self.port) + "," + self.hash
