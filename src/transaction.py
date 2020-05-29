import config
from hash import make_hash

class Transaction:
  self.to = ''
  self.from = ''
  self.amount = 0
  self.type = 1
  self.hash = ''
  self.signature = ''
  self.extra = ''
  self.fee = 0.5 * SINGLETON_COLLECTION_AMOUNT
  def __init__(to, from, amount, type=1, hash='', signature='', extra='', fee=0.5 * SINGLETON_COLLECTION_AMOUNT):
    self.to = to
    self.from = from
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
  def sign(priv_key):
    pass
  def valid(self):
    return True
  def read(self, hash):
    return self
  def save(self):
    return True
  def as_bytes(self):
    return "{}{}{}{}{}{}".format(to, from, amount, type, extra, fee)
