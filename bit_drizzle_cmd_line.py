'''
BitDrizzle - Small, academic DHT based P2P system
Supports network operations of find_peer, lookup and insert
Supports data operation of writing to a key value store

Written by John Pecarina, Air Force Institute of Technology,
john.pecarina@afit.edu
Feb 1 2016

Modified by Colin Busho, Kevin Cooper, Paul Jordan, and Chip Van Patten
Last Modified:  14 Feb 2016
'''
import time

from app_support.bd_api import BitDrizzle


def print_command_line_help():
    print("H - Help Menu")
    print("LL - Local Listener: Checks if the Drizzler app_support listener is listening for commands")
    print("MM - Multi Mode: Makes the program set up all network nodes")
    print("FN - Find Network: Enter FN, future options could be host and/or port range, sets an EntryNode")
    print("LH - Locate Hash: Enter LH with a hash value, as a search function in the network")
    print("JN - Join Network: Enter JN, no options, will enter the host through Entry Node, sets routing information")
    print("LN - Leave Network: Enter LN, no options, will leave the network, removes routing info")
    print("SZ - Get Network Size: Enter SZ, no options, will send a message to estimate size of the network")
    print("RI - Print Routing Info: Enter RI, no options, will print the routing info for this node")
    print("W - Write Data: Enter W, with options Ex: WL <filename=test_file.txt> <piece_size=256>")
    print("                         - option L for app_support, N for network, stores data to app_support or network store")
    print("                         - filename default is test_file.txt, piece_size default is 256 chars (bytes)")
    print("R - Read Data:  Enter R, with options Ex: RN <key>  (read data from network at key)")
    print("                         - option L for app_support, N for network, reads data from app_support or network store")
    print("                         - option K takes a key, default is test_key entry in config.py")
    print("D - Delete Data:  Enter D, with options Ex: DN <key>  (delete data from network at key)")
    print("                         - option L for app_support, N for network, deletes data from app_support or network store")
    print("                         - option K takes a key, default is test_key entry in config.py")
    print("X - Exit BitDrizzle: Just exits the app")

def file_reader(file_name):
    file_contents = ""
    #opening the file
    with open('test_file.txt', 'r') as myfile:
        #read all the bytes and replace line returns with a blank
        file_contents=myfile.read().replace('\n', '')
    return file_contents


import config

'''
Main program:
'''
def main():
    import os
    os.system("mode con: cols=120 lines=75")
    print("Welcome to BitDrizzle CLI!")
    bd = BitDrizzle()

    print("Binding to ports in Drizzler setup and start all servers")
    bd.drizzlerSetup()

    print("Setting up app_support head")
    bd.localSetup()

    print("#######################################################################")
    print("#                            BIT DRIZZLE 1.0                          #")
    print("#                           CMD LINE INTERFACE                        #")
    print("#######################################################################")

    while True:
        cmd_string = input("Enter a command or type H for help: " or "!")
        if not (len(cmd_string) == 0):
            cmd = cmd_string.upper().split()
            if cmd[0] == 'H':
                print_command_line_help()
            elif cmd[0] == 'LL':
                if bd.is_cmd_ready():
                    print("Drizzler is listening for commands")
                else:
                    print("No services")
            elif cmd[0] == 'MM':
                print("Going multi mode...")
                print(bd.go_multi_mode())
            elif cmd[0] == 'FN':
                print("Found network at: " + bd.find_net())
            elif cmd[0] == 'LH':
                try:
                    print(bd.locate_hash(cmd[1]))
                except Exception as e:
                    print(bd.locate_hash(config.test_key))
            elif cmd[0] == 'JN':
                print(bd.join_net())
            elif cmd[0] == 'RI':
                try:
                    print(bd.get_net_neighbors(cmd[1]))
                except Exception as e:
                    print(bd.get_net_neighbors("FULL"))
            elif cmd[0] == 'LN':
                print("Leave Network")
            elif cmd[0] == 'SZ':
                print("Get Network Size")
            elif cmd[0] == 'WL':
                file_contents = ""
                try:
                    file_contents = file_reader(cmd[1])
                except Exception as e:
                    file_contents = file_reader(config.data_file)
                try:
                    piece_size = str(cmd[2])
                except Exception as e:
                    piece_size = config.piece_size
                print(bd.write_local(file_contents, piece_size))
            elif cmd[0] == 'WN':
                file_contents = ""
                try:
                    file_contents = file_reader(cmd[1])
                except Exception as e:
                    file_contents = file_reader(config.data_file)
                try:
                    piece_size = str(cmd[2])
                except Exception as e:
                    piece_size = config.piece_size
                print(bd.write_to_net(file_contents, piece_size))
            elif cmd[0] == 'R':
                print("Read Data")
            elif cmd[0] == 'D':
                print("Delete Data")
            elif cmd[0] == 'LD':
                print(bd.local_dump().encode('cp437', errors='replace'))
            elif cmd[0] == 'PD':
                print(bd.peer_dump().encode('cp437', errors='replace'))
            elif cmd[0] == 'X':             #just a hard crash really
                print("Exiting Application")
                time.sleep(1)
                os._exit(0)
            else:
                print("Command Not Found")



# main entry point to program
if __name__ == "__main__":
    main()
