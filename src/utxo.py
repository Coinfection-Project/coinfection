'''
UTXO this file defines the txin and txout structs
'''
from hash import make_hash
from config import SINGLETON_COLLECTION_AMOUNT, TOKEN_INFECTION_CLUMP
class txIn:
  hash = '' # transaction input hash: sha256 (transaction + index + amount + address)
  tx_hash = '' # the hash of the transaction this input is soruced from
  index = 0 # the index of the output in the tx specifyed in tx_hash
  address = '' # the owners address (pubkey)
  amount = 0 # the amount (in singleton units)
  signture = '' # the self.hash var signed with owner address's priv key 
  def __init__(self, hash='', tx_hash='', amount=0, signature='', owner='' index=0):
    self.hash = hash
    self.tx_hash = tx_hash
    self.amount = amount
    self.index = index
    self.address = ownder
    self.signature = signature
  def to_json(self):
    return '{ "hash" : "{}", "tx_hash" : "{}", "amount" : {}, "index" : {}, "address" : "{}", "signature: "{}" }'.format(self.hash, self.tx_hash, self.amount, self.index, self.address, self.signature)
  
  def from_json(self, json):
    obj = json.loads(json)
    self.hash = obj['hash']
    self.tx_hash = obj['tx_hash']
    self.amount = obj['amount']
    self.index = obj['index']
    self.address = obj['ownder']
    self.signature = obj['signature']
    
  def as_bytes(self):
    return "{}{}".format(self.output_hash,self.amount)
  
  def hash(self):
    work = self.as_bytes()
    self.hash = make_hash(work)
    return self.hash
  
  def sign(self):
    
    
class txOut:
  hash = '' # the hash of the index and the owners addr
  index = 0x00000000 # the index of this output
  address = '' # the address (hex encoded pubkey) of the owner of this output
  amount = 0 # the amount this output is worth (in singleton units)
  allowed_infection = False # if this output has been set to be infectable
  immune = False # if this output is recovered and immune
  infected  = False # if this output is infected
  
  def __init__(self, hash='', index=0x00000000, owner='', amount=0, allowed_infection=False, immune=False):
    self.hash = hash
    self.index = index
    self.address = owner
    self.amount = amount
    self.immune = immune
    self.allowed_infection = allowed_infection
  
  def is_clump(self): # returns true if this is a token clump
    return (self.amount == SINGLETON_COLLECTION_AMOUNT * TOKEN_INFECTION_CLUMP)
  
  def is_infectable(self):
    return (self.is_clump() == True and self.allowed_infection == True and self.immune == False and self.infected == False)
  
  

