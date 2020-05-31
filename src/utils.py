from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import time as time_ #make sure we don't override time

class Wallet:
  balance = 0
  outputs = []
  pubkey = ''
  privkey = ''
  address = ''
  def __init(balance=0, outputs=[], pubkey='', privkey='', address=''):
    self.balance = balance
    self.outputs = outputs
    self.pubkey = pubkey
    self.privkey = privkey
    self.address = address
  def gen_keypair(self):
    self.privkey = Ed25519PrivateKey.generate()
    self.pubkey = self.privkey.public_key()
    self.address = self.pubkey.public_bytes(
      encoding=serialization.Encoding.Raw,
      format=serialization.PublicFormat.Raw
    ).hex()

# thanks to https://stackoverflow.com/a/6000198
def millis():
    return int(round(time_.time() * 1000))
