import hashlib

chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f']# Hexadecimal

def make_hash(text):
    '''
    Convert a string into a SHA-256 hash
    '''
    m = hashlib.sha256()
    m.update(text.encode("utf-8"))
    m.update(str(m.hexdigest()).encode("utf-8"))
    return str(m.hexdigest())

def fast_hash(text):
	'''
    Convert a string into a BLAKE2 hash
    '''
    m = hashlib.blake2b(digest_size=128) # this hash function is used for the db (to hash the keys). it is extra large (128 bytes) to prevent collisions
    m.update(text.encode("utf-8"))
    m.update(str(m.hexdigest()).encode("utf-8"))
    return str(m.hexdigest())

def test():
	print(make_hash(input("$:")))
