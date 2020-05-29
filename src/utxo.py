'''
UTXO this file defines the txin and txout structs
'''

class txIn:
  output_hash = ''
  amount = 0
  signature = ''
  def __init(self, output_hash='', amount=0, signature=''):
    self.output_hash = output_hash
    self.amount = amount
    self.signature = signature
    
  def as_bytes(self):
    return "{}{}".format(self.hash,self.amount)
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
