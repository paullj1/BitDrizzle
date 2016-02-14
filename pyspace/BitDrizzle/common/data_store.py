import hashlib      #used for md5 hash

# class for a generic string based key-value store
class DataItem():

    # Constructor for a data item which is a value and the hash of that value
    def __init__(self, value):
        self.value = value
        self.key = self.getHash(value)

    # uses an MD5 hash function to return the key of the value string
    def getHash(self, value):
        id_string = self.value
        return hashlib.md5(id_string.encode('utf-8')).hexdigest()

'''
    This class specifies the data storage for the node.
'''
class Data():

    # Constructor
    def __init__(self):
        self.data = {}     # data storage using (key, value) pairs

    # Writes a data item into this nodes hash table
    def write(self, d_item_key, d_item_value):
        try:
            # write the data item with updated counts
            self.data[d_item_key] = d_item_value
            return "OK"
        except:
            return "failed write"

    def read(self, d_item_key):
        try:
            return self.data[d_item_key]
        except:
            return "failed read"
    # to string function
    def __str__(self):
        if bool(self.data):
            return ('\n'.join("{!s},{!r}".format(k,v) for (k,v) in self.data.items()))
        return "Data is empty"
