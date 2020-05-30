import random
from hash import make_hash
import hashlib
from config import *
from transaction import *
import sys

max_nonce = 2 ** 32

'''
A block.
'''
class Block:
	height = 0
	hash = ''
	diff_bits = 1
	timestamp = 0
	transactions = []
	nonce = 0x00
	version = 0x111
	prev_hash = ''
	def __init__(self, height=0, hash='', diff_bits=1, timestamp=0, transactions=[], nonce=0, version=100, prev_hash='00000000000000000000000000000000'):
 		self.hash = hash
 		self.height = height
 		self.diff_bits = diff_bits
 		self.timestamp = timestamp
 		self.nonce = nonce
 		self.transactions = transactions
 		self.version = version
 		self.prev_hash = prev_hash
    
	def mine(self, difficulty, diff_bits=None):
		if (diff_bits != None):
			if (diff_bits < difficulty): # diff bits must be over or equal to difficulty
				return 'diff_bits too low'
			elif (diff_bits > 0):
 				return 'bad diff_bits'
			else:
				# set self diff bits to the specifyed diff_bits
				self.diff_bits = diff_bits
		else:
			# set the target diff bits to the minimum difficulty (difficulty var)
			self.diff_bits = difficulty
			if (len(self.transactions) > 1):
				if (self.transactions[0].type != 1):
					amount = BLOCK_REWARD
					coinbase_txn = coinbase(MINING_ADDR, amount)
					tmp = self
					for i in range(len(self.transactions)):
						if (i == 0):
							tmp.transactions[0] = coinbase_txn
						else:
							tmp.transactions[i] = self.transactions[i-1]
					tmp.transactions.push(self.transactions[-1])
					self.transactions = tmp.transactions
			else:
				self.transactions[0] = coinbase(MINING_ADDR, BLOCK_REWARD)
			work = self.as_bytes()
			target = 2 ** (256-self.diff_bits)
			for nonce in range(max_nonce):
				# increment the nonce
				self.nonce = nonce
				# hash the block
				hash_result = make_hash(work)
            	# check if this is a valid result, below the target
				if int(hash_result, 16) < target:
					#  set the hash of self to the hash we found
					self.hash = str(hash_result)
					return None		
	def as_bytes(self):
		out = "{}{}{}{}{}{}{}".format(self.height, self.diff_bits, self.timestamp, self.nonce, self.transactions, self.version, self.prev_hash)
		return out
	def valid(self):
		if self.hash == '': # a hash should never be blank
			return 'empty hash'
		else:
			tmp = self # clonse self into a temp block buffer
			tmp.hash() # hash the temp block buffer
			if (tmp.hash != self.hash): # if the temp block resultant hash is not that of self.hash return err
				return 'bad block hash'
		if (self.height < 0): # check nonce is postive
			return 'negative nonce'
		else:
			tmp = Block() # create shell block
			read_err = tmp.read(hash=self.prev_hash) # try to read the block with hash self.prev_hash into the shell block
			if (read_err != None): # if it failed return
				return 'failed to read prev block. error='+read_err
			elif (tmp.height != self.height-1): # if the read block's height is not 1 behind self.height return err'
				return 'height missmatch'
		if (int(self.hash, 16) < self.diff_bits): # check the diff bits and the hash match up
			return 'hash difficulty low'
		elif (False): # todo: check if diff bits is over or equal to difficulty for height self.height 
			return 'diff bits low'
		else:
			i = 0
			for tx in self.transactions:
				i = i+1
				if (tx.valid() == False):
					return 'tx at slot=' + i + ' invalid'
		if (sys.sizeof(self) > MAX_BLOCK_SIZE): # check size of block
			return 'block too big'

	def hash_blk(self):
		work = self.as_bytes()
		self.hash = make_hash(work)
		return self.hash()
def coinbase(miner, reward=BLOCK_REWARD):
		txn = Transaction(type=0, sender='coinbase', to=miner, amount=reward, fee=0)
		txn.hash_tx()
		return txn
def genesis():
		gen_blk = Block(timestamp=time.time()*1000)
		gen_blk.transactions = coinbase(GENESIS_REWARD_ADDR, PREMINE)
		gen_blk.mine()
