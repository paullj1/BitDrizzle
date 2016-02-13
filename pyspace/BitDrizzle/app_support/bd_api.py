import time
import config
from app_support.local_head import LocalHead
from peer.peer_head import Drizzler

class BitDrizzle:

    def __init__(self):
        self.host = config.host
        self.peer_port = config.base_peer_port       #we don't know until we try to bind to it
        self.local_port = config.base_local_port     #we don't know until we try to bind to it
        self.myNode = None
        return

    def drizzlerSetup(self):
        MM = 0 # multi mode flag off
        #the drizzler_thread is of the drizzler class within peer head,
        # it guides the construction of the net facing node ( kwargs are a place holder, not used )
        # the args it takes are for unique ports (peer and app_support, a start port and the net size
        while self.peer_port < (config.base_peer_port + config.net_size):
            try:
                drizzler_thread = Drizzler(args=(self.host, self.peer_port, self.local_port,
                                             config.base_peer_port, config.net_size, MM), kwargs={'a':'A', 'b':'B'})
                #start the thread
                drizzler_thread.start()
                break
            except:
                self.peer_port = self.peer_port + 1
                self.local_port = self.local_port + 1
        return

    def localSetup(self):
        self.myNode = LocalHead(self.host, self.local_port) # this is the app_support hash table and a listener port
        return

    def go_multi_mode(self):
        # MM only works from the node at the base_port
        MM = 1 # multi mode flag
        if self.peer_port == config.base_peer_port:
            threads = []    # a container for threads, which we may or may not attempt to search
            # we'll simulate the growth of the network with the building of threads, net_size of them in this case
            peer_port = self.peer_port + 1
            local_port = self.local_port + 1
            while peer_port < (config.base_peer_port + config.net_size):
                print(peer_port)
                try:
                    #the drizzler_thread is of the drizzler class within peer head,
                    # it guides the construction of the net facing node ( kwargs are a place holder, not used )
                    # the args it takes are for unique ports (peer and app_support, a start port and the net size
                    drizzler_thread = Drizzler(args=(self.host, peer_port, local_port,
                                                 config.base_peer_port, config.net_size, MM), kwargs={'a':'A', 'b':'B'})
                    #add the thread to the container, it will be indexed by i, the offset of the port number, if it s needed
                    threads.append(drizzler_thread)
                    #start the thread, which doesn't happen right away
                    drizzler_thread.start()
                    #we sleep so a thread can take control

                    # starting them in order will generally allow them to
                    # insert into the network in order
                    time.sleep(.1)
                    # However, if the time is set below 0.1, then the threads may conflict with each other
                    # and instead of one large network, many little networks will emerge

                except Exception as e:
                    print(e)

                peer_port = peer_port + 1
                local_port = local_port + 1

            # this particular thread will wait for the network setup to conclude
            print("Standby...")
            # I suggest setting net_size to 10 or less for development and sleep to 3 seconds
            time.sleep(3)
        return "ALL NETWORK NODE THREADS HAVE STARTED"


    # P2P Networking API
    def is_cmd_ready(self):
        return self.myNode.hasListener()

    def get_net_neighbors(self, mode):
        return self.myNode.getNeighbors(mode)

    def find_net(self):
        return self.myNode.findPeer()

    def locate_hash(self, hash):
        return ("Hash " + hash + " is at " + self.myNode.locateHash(hash))

    '''
    #
    #
    #  NETWORKING API THAT NEEDS TO BE IMPLEMENTED
    #
    '''
    def join_net(self):
        return self.myNode.joinNetwork()

    def remove_from_net(self):
        return

    def get_net_size(self):
        return

    def set_new_net_size(self):
        return

    # data management API
    def write_to_net(self, data_string, piece_size):
        start_time = time.time()
        parts = int(len(data_string) / piece_size)
        last_part = int(len(data_string) % piece_size)
        # write the full pieces
        for i in range(0, parts):
            piece = data_string[(i*piece_size):(i*piece_size)+piece_size]
            self.myNode.writeToNet(piece)
        # write the last piece (the remainder)
        last_piece = data_string[len(data_string)-last_part:len(data_string)]
        self.myNode.writeToNet(last_piece)
        total_real_time = time.time() - start_time
        total_parts = parts + 1
        total_bytes = len(data_string)
        return ("Wrote " + str(total_bytes) + " bytes with " + str(total_parts) +
                    " parts in " + str(total_real_time) + " seconds")

    def write_local(self, data_string, piece_size):
        start_time = time.time()
        parts = int(len(data_string) / piece_size)
        last_part = int(len(data_string) % piece_size)
        # write the full pieces
        for i in range(0, parts):
            piece = data_string[(i*piece_size):(i*piece_size)+piece_size]
            self.myNode.writeLocal(piece)
        # write the last piece (the remainder)
        last_piece = data_string[len(data_string)-last_part:len(data_string)]
        self.myNode.writeLocal(last_piece)
        total_real_time = time.time() - start_time
        total_parts = parts + 1
        total_bytes = len(data_string)
        return ("Wrote " + str(total_bytes) + " bytes with " + str(total_parts) +
                    " parts in " + str(total_real_time) + " seconds")

    def local_dump(self):
        return self.myNode.DumpLocalData()

    def peer_dump(self):
        return self.myNode.DumpPeerData()

    '''
    #
    #  DATA MANAGEMENT API TO IMPLEMENT
    #
    '''

    def read_from_net(self, hash_code):
        return self.myNode.readFromNet(hash_code)

    def read_local(self):
        return

    def delete_from_net(self, hash_code):
        return self.myNode.deleteFromNet(hash_code)

    def delete_local(self):
        return


