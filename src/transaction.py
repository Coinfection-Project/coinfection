import config
from hash import make_hash
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import db
import json

class Transaction:
  self.to = ''
  self.sender = ''
  self.amount = 0
  self.type = 1
  self.hash = ''
  self.signature = ''
  self.extra = ''
  self.fee = 0.5 * SINGLETON_COLLECTION_AMOUNT
  
  def __init__(to, sender, amount, type=1, hash='', signature='', extra='', fee=0.5 * SINGLETON_COLLECTION_AMOUNT):
    self.to = to
    self.sender = sender
    self.amount = amount
    self.type = type
    self.hash = hash
    self.signature = signature
    self.extra = extra
    self.fee = fee
    
  def hash(self):
    work = self.as_bytes()
    self.hash = make_hash(work)
    return self.hash
  
  def sign(self, priv_key):
    key = ed25519.Ed25519PrivateKey.from_private_bytes(bytearray.fromhex(priv_key).decode())
    self.signature = key.sign(self.hash.encode('utf-8')).hex()
    return self.signature
  
  def valid(self):
    return True
  
  def read(self, hash):
    return self
  
  def save(self):
    db.set(key=self.hash, value=self.ser(), path='txn.db')
    return True
  
  def as_bytes(self):
    return "{}{}{}{}{}{}".format(to, sender, amount, type, extra, fee)
  
  def ser(self):
    return json.dumps(self.__dict__)
  
  def valid_sig(self):
    if (self.sender == 'coinbase'):
      return True
    else:
      if (self.sender.endswith('.coof')):
        read = db.get(key=self.sender, path='nicknames.db')
        if (read == None):
          return False;
        else:
          public_key =  ed25519.Ed25519PublicKey.from_public_bytes(bytearray.fromhex(read).decode())
      else:
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(bytearray.fromhex(self.sender).decode())
      try:
        public_key.verify(signature, self.hash.encode('utf-8'))
        return True
      except:
        return False
