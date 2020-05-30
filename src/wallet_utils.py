from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

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
