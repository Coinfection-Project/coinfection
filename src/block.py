import random
from hash import make_hash

Class Block:
	height = 0
  hash = ''
  diff_bits = 1
  timestamp = 0
  transactions = []
  nonce = 0x00
  version = 0x111
  prev_hash = ''
  
 	def __init__(self, height=0, hash='', diff_bits=1, timestamp=0, transactions=[], nonce=0, version=100, prev_hash=''):
  	self.hash = hash
		self.height = height
 		self.diff_bits = diff_bits
    self.timestamp = time
    self.nonce = nonce
		self.transactions = transactions
    self.version = version
    self.prev_hash = prev_hash
    
	def hash(self, difficulty, diff_bits=None):
		if (diff_bits != None):
			if (diff_bits < difficulty):
				return 'diff_bits too low'
			elif (diff_bits > 0):
 				return 'bad diff_bits'
			else:
				self.diff_bits = diff_bits
    else:
			self.diff_bits = difficulty
		work = self.as_bytes()
    while True:
			haah = make_hash( work )
			while not( match( self.diff_bits, hash ) ): # Repeats until find a valid hash
				self.nonce = self.nonce + 1
        work = self.as_bytes()
			self.hash = hash
