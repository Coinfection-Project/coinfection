'''
UTXO this file defines the txin and txout structs
'''
from hash import make_hash

class txIn:
  hash = ''
  output_hash = ''
  amount = 0
  signature = ''
  def __init(self, hash='', output_hash='', amount=0, signature=''):
    self.hash = hash
    self.output_hash = output_hash
    self.amount = amount
    self.signature = signature
    
  def as_bytes(self):
    return "{}{}".format(self.output_hash,self.amount)
  def hash(self):
    work = self.as_bytes()
    self.hash = make_hash(work)
    return self.hash
    
class txOut:
  hash = ''
  index = 0x00000000
  owner = ''
  def __init(self, hash='', index=0x00000000, owner=''):
    self.hash = hash
    self.index = index
    self.owner = owner
  
  def as_bytes(self):
    return "{}{}".format(self.index,self.owner)
  def hash(self):
    work = self.as_bytes()
    self.hash = make_hash(work)
    return self.hash
