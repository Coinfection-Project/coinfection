'''
UTXO this file defines the txin and txout structs
'''
from hash import sha256
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from config import SINGLETON_COLLECTION_AMOUNT, TOKEN_INFECTION_CLUMP
import json
from db import get, set
class txIn:
    # transaction input hash: sha256 (transaction + index + amount + address)
    hash = ''
    tx_hash = ''  # the hash of the transaction this input is soruced from
    index = 0  # the index of the output in the tx specifyed in tx_hash
    address = ''  # the owners address (pubkey)
    amount = 0  # the amount (in singleton units)
    signture = ''  # the self.hash var signed with owner address's priv key

    def __init__(self, hash='', tx_hash='', amount=0, signature='', owner='', index=0):
        self.hash = hash
        self.tx_hash = tx_hash
        self.amount = amount
        self.index = index
        self.address = owner
        self.signature = signature

    def to_json(self):
        as_json =  ' "hash" : "{}", "tx_hash" : "{}", "amount" : {}, "index" : {}, "address" : "{}", "signature": "{}" '.format(self.hash, self.tx_hash, self.amount, self.index, self.address, self.signature)
        return "{" + as_json + "}"
        
    def from_json(self, as_json):
        obj = None
        if (isinstance(as_json, str)):
            obj = json.loads(as_json)
        else:
            obj = as_json
        self.hash = obj['hash']
        self.tx_hash = obj['tx_hash']
        self.amount = int(obj['amount'])
        self.index = int(obj['index'])
        self.address = obj['address']
        self.signature = obj['signature']

    def as_bytes(self):
        return "{}{}{}{}".format(self.tx_hash, self.amount, self.index, self.address)

    def hash_in(self):
        work = self.as_bytes()
        self.hash = sha256(work)
        return self.hash

    def sign(self, priv_key):
        key = Ed25519PrivateKey.from_private_bytes(
            bytearray.fromhex(priv_key).decode())
        self.signature = key.sign(self.hash.encode('utf-8')).hex()
        return self.signature
    
    def valid_signature(self):
        if (self.owner == 'coinbase'):
            return True
        else:
            # all nicknames end with .coof, if the owner ends with .coof then we need to get the pubkey from the db
            if (self.owner.endswith('.coof')):
                read = get(key=self.owner, collection_name='nicknames.db')
                if (read == None):
                    return False
                else:
                    public_key = Ed25519PublicKey.from_public_bytes(
                        bytearray.fromhex(read).decode())
            else:
                public_key = Ed25519PublicKey.from_public_bytes(
                    bytearray.fromhex(self.owner).decode())
            try:
                public_key.verify(bytearray.fromhex(
                    self.signature).decode(), self.hash.encode('utf-8'))
                return True
            except:
                return False

    def coinbase(self):
        if self.tx_hash != '':
            return False
        elif self.address != 'coinbase':
            return False
        else:
            return True


class txOut:
    hash = ''  # the hash of the index and the owners addr
    index = 0x00000000  # the index of this output
    # the address (hex encoded pubkey) of the owner of this output
    address = ''
    amount = 0  # the amount this output is worth (in singleton units)
    allowed_infection = False  # if this output has been set to be infectable
    immune = False  # if this output is recovered and immune
    infected = False  # if this output is infected

    def __init__(self, hash='', index=0x00000000, owner='', amount=0, allowed_infection=False, immune=False):
        self.hash = hash
        self.index = index
        self.address = owner
        self.amount = amount
        self.immune = immune
        self.allowed_infection = allowed_infection

    def to_json(self):
        as_json =  ' "hash" : "{}", "index" : {}, "address" : "{}", "amount" : {}, "allowed_infection" : "{}", "immune": "{}" '.format(self.hash, self.index, self.address, self.amount, self.immune, self.allowed_infection)
        return "{" + as_json + "}"
        
    def from_json(self, as_json):
        obj = None
        if (isinstance(as_json, str)):
            obj = json.loads(as_json)
        else:
            obj = as_json
        self.hash = obj['hash']
        self.index = int(obj['index'])
        self.address = obj['address']
        self.amount = int(obj['amount'])
        self.immune = bool(obj['immune'])
        self.allowed_infection = bool(obj['allowed_infection'])

    def is_clump(self):  # returns true if this is a token clump
        return (self.amount == SINGLETON_COLLECTION_AMOUNT * TOKEN_INFECTION_CLUMP)

    def is_infectable(self):
        return (self.is_clump() == True and self.allowed_infection == True and self.immune == False and self.infected == False)

    def as_bytes(self):
        return "{}{}{}".format(self.index, self.address, self.amount)

    def hash_out(self):
        work = self.as_bytes()
        self.hash = sha256(work)
        return self.hash

    def save(self):
        return set(self.hash, self.to_json(), 'utxos')
    
    def get(self,hash):
        got = get(hash, 'utxos')
        try:
            self = self.from_json(got)
        except:
            return False
        return True
