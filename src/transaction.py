import config
from hash import make_hash
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import db
import json
from utils import listToString

class Transaction:
  to = ''
  sender = ''
  amount = 0
  type = 1
  hash = ''
  signature = ''
  extra = ''
  fee = 0.5 * config.SINGLETON_COLLECTION_AMOUNT
  inputs = []
  outputs = []
  
  def __init__(self, to, sender, type=1, hash='', signature='', extra='', fee=0.5 * config.SINGLETON_COLLECTION_AMOUNT, inputs=[], outputs=[]):
    self.to = to
    self.sender = sender
    self.type = type
    self.hash = hash
    self.inputs = inputs
    self.outputs = outputs
    self.signature = signature
    self.extra = extra
    self.fee = fee
  
  def hash_tx(self):
    work = self.as_bytes()
    self.hash = make_hash(work)
    return self.hash
  
  def sign(self, priv_key):
    key = ed25519.Ed25519PrivateKey.from_private_bytes(bytearray.fromhex(priv_key).decode())
    self.signature = key.sign(self.hash.encode('utf-8')).hex()
    return self.signature
  
  def valid(self):
    # TODO
    return True
  
  def read(self, hash):
    return self
  
  def save(self):
    db.set(key=self.hash, value=self.ser(), path='txn.db')
    return True
  
  def as_bytes(self):
    return "{}{}{}{}{}{}{}".format(self.to, self.sender, listToString(self.inputs), listToString(self.outputs), self.type, self.extra, self.fee)
  
  def ser(self):
    return json.dumps(self.__dict__)
  
  def valid_signature_raw(sig, pub, text): # takes a hex sig and a hex pub key as well as the input plaintext (as raw string)
    public_key =  ed25519.Ed25519PublicKey.from_public_bytes(bytearray.fromhex(pub).decode())
    try:
      public_key.verify(bytearray.fromhex(self.signature).decode(), text.encode('utf-8'))
      return True
    except:
      return False
  def valid_input(self, index):
    return True # TODO
  
  def valid_sig(self):
    if (self.sender == 'coinbase'):
      return True
    else:
      if (self.sender.endswith('.coof')): # all nicknames end with .coof, if the sender ends with .coof then we need to get the pubkey from the db
        read = db.get(key=self.sender, path='nicknames.db')
        if (read == None):
          return False;
        else:
          public_key =  ed25519.Ed25519PublicKey.from_public_bytes(bytearray.fromhex(read).decode())
      else:
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(bytearray.fromhex(self.sender).decode())
      try:
        public_key.verify(bytearray.fromhex(self.signature).decode(), self.hash.encode('utf-8'))
        return True
      except:
        return False
