BitDrizzle is a small DHT based system to investigate issues in distributed systems

In its current form it supports the following
1. A command line interface
2. An application programming interface to interact with local and net-facing data functionality
3. An application programming interface to interact with peers in a p2p network
4. Basic DHT networking architecture with succ/pred neighbors for ring based networking
5. Basic routing functions for finding a peer, lookup(hash) and insert into the network
6. Basic data writing functions for writing to local and stable network hash tables
7. Single mode and multi mode operation, supported by multithreaded architecture

To install, download and extract files to a directory

To configure, open the config.py file in a text editor and change basic settings

To run, execute bit_drizzle_cmd_line.py and type H, for example:

Enter a command or type H for help:
H - Help Menu
LL - Local Listener: Checks if the Drizzler app_support listener is listening for commands
MM - Multi Mode: Makes the program set up all network nodes
FN - Find Network: Enter FN, future options could be host and/or port range, sets an EntryNode
LH - Locate Hash: Enter LH with a hash value, as a search function in the network
JN - Join Network: Enter JN, no options, will enter the host through Entry Node, sets routing information
LN - Leave Network: Enter LN, no options, will leave the network, removes routing info
SZ - Get Network Size: Enter SZ, no options, will send a message to estimate size of the network
RI - Print Routing Info: Enter RI, no options, will print the routing info for this node
W - Write Data: Enter W, with options Ex: WL <filename=test_file.txt> <piece_size=256>
                         - option L for app_support, N for network, stores data to app_support or network store
                         - filename default is test_file.txt, piece_size default is 256 chars (bytes)
R - Read Data:  Enter R, with options Ex: RN <key>  (read data from network at key)
                         - option L for app_support, N for network, reads data from app_support or network store
                         - option K takes a key, default is test_key entry in config.py
D - Delete Data:  Enter D, with options Ex: DN <key>  (delete data from network at key)
                         - option L for app_support, N for network, deletes data from app_support or network store
                         - option K takes a key, default is test_key entry in config.py
X - Exit BitDrizzle: Just exits the app


Steps to add functionality:

1. Add command in CLI and test CLI by printing call to console
2. Add stub method in API and call it from the CLI, printing string to console
3. Add to new method in API so it calls a stub in local_head, printing string to console
4. Create a client and a message in local_head, return the message to see it's format in the console
5. Use the new client in local_head to send the message to the local listener, should return "OK" in the console
6. Add a stub handler in listener's perform action that accepts the message and parses it, return what you want to verify
7. Add a stub method in peer_head or router that returns a test string, call the message in perform action, run to verify
8. Add functionality in peer_head or router, peer_head could be the interface for calls to data, router for calls to other servers
9. As functionality is added, track progress in the console interface, may need to add functionality in methods in the chain
10. Develop and Test with the SM or MM with net_size set to 2 in the config.py file, expand as you go



Future Extensions
This code base might be adapted for many purposes. They are listed here to remind you of the course material and inspire you in your projects:
1)	Port to real networks. Changing this to work for Rasp Pi over WiFi or among a network of virtual machines will involve some tweaking. One change will be to replace the broadcast function for ports to one for IPs. 
2)	Topology Management. Use a network management layer that changes the topology of the underlying P2P network or find ways to build routing trees. 
3)	Hybrid Architectures. Combining P2P networks and client-broker-server paradigms can result in varied topologies that may be tailored for a particular setting of your interest.
4)	Virtualization. Simulate the addition of new nodes in the network to handle load balancing of data items when required. When is it appropriate to add or remove nodes?
5)	Parallelization. Use the code base to distribute data to various processing nodes. Each processing node can have its own processing service that executes an operation on the data and returns a message with the results. One could even migrate code and processes to nodes where data processing is building up.
6)	Multithreading and synchronization. The client lookups, writes and reads could all be multithreaded to speed up processing if the nodes are on their own system. Multithreading and the possibility of multiple server requests in a real network will require synchronization variables so that nodes can have many open connections and many concurrent processes.
7)	Improved lookup. Chord enables this with finger tables that address with logarithmic scale, Kadmelia adds the XOR function. These methods require a finger table and function that constantly updates.
8)	Random P2P systems. Abandon hash codes and just choose your neighbors at random or using the small world approach. Investigate the effects of using various probability distribution functions and node degrees.
9)	Information Dissemination. Add a gossip protocol or a gossip protocol with rumor mongering to improve communications usage over the flooding approach.
10)	Clock Synchronization. Send clock values through the network, track drift over time and determine ways to adjust them.
11)	Total Ordering. Forget making clocks the same, but determine how to implement a system that ensures events are ordered even if the timestamps are wrong.
12)	Detecting and handling node failures. Either are tough problems. One, because the pred/succ links would be broken. Two, because data could be permanently lost. Three, because it could be disrupting service for users. 
13)	Distributed Snapshot. Take a picture of the network and restore to that point at some arbitrary time. 
14)	Distributed Transactions. Use the P2P network to build a P2P financial transaction system. Need an example? Read up on BitCoin.
15)	Replication. Replication is good for networks that have a large number of reads. It also helps add robustness. However, tracking, storing and retrieving duplicates is not trivial. 
16)	Distributed file or databases.  Using the DHT, you can route messages that call other API’s. A trivial example is sending a http query and having the receiving node call it. File system access and database access can use similar command encapsulation to add easy functionality to your P2P network.
17)	Dropbox like folder synching. If you have the P2P network set up with file system calls, it would take a few minor steps for building a program that monitors file folders and then sends new files into the DHT for storage. Load a new computer with the same client to get the folder synched.
18)	Bittorrent like content distribution. Storing a file means splitting it into parts. Retrieving a file means getting the file of hash references, retrieving them all and then assembling.
19)	Authentication. You can use encryption and key distribution to make sure no one gets into your services but your authorized clients.

