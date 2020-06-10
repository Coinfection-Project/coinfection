import random
from hash import make_hash
import hashlib
from config import *
from transaction import Transaction
import sys
from difficulty import diff2target, check_diff
import json as j
from db import get, set
import time
from utxo import txIn, txOut
import logging
from utils import millis

max_nonce = 2 ** 32

log = logging.getLogger(__name__)

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

	def to_json(self):
			txns_json = '[ '
			i = 0
			for txn in self.transactions:
				i += 1
				txn_json = txn.to_json()
				txns_json = txns_json + txn_json
				if (i != len(self.transactions)):
					txns_json += ', '
			txns_json = txns_json + ']'

			return '{ ' + '"hash" : "{}", "height"  : {}, "diff_bits" : {}, "timestamp" : {}, "nonce" : {}, "transactions" : {}, "version" : {}, "prev_hash" : "{}" '.format(self.hash, self.height, self.diff_bits, self.timestamp, self.nonce, txns_json, self.version, self.prev_hash) + '}'

	def from_json(self, as_json):
			log.debug("Json decoding block, json="+as_json)
			obj=j.loads(as_json)
			self.hash=obj['hash']
			self.height=obj['height']
			self.diff_bits=obj['diff_bits']
			self.timestamp=obj['timestamp']
			self.nonce=obj['nonce']
			for txn_json in obj['transactions']:
				txn= Transaction(to='', sender='')
				txn.from_json(txn_json)
				self.transactions.append(txn)

			self.version=obj['version']
			self.prev_hash=obj['prev_hash']

	def mine(self, difficulty, diff_bits=None):
		if (diff_bits != None):
			if (diff_bits < difficulty):  # diff bits must be over or equal to difficulty
				return 'diff_bits too low'
			elif (diff_bits > 0):
 				return 'bad diff_bits'
			else:
				# set self diff bits to the specifyed diff_bits
				self.diff_bits=diff_bits
		else:
			# set the target diff bits to the minimum difficulty (difficulty var)
			self.diff_bits=difficulty
			txn_count = 0
			for _ in self.transactions:
				txn_count += 1
			if (txn_count > 1):
				if (self.transactions[0].type != 1):
					amount=BLOCK_REWARD
					coinbase_txn=coinbase(MINING_ADDR, amount)
					tmp=self
					for i in range(len(self.transactions)):
						if (i == 0):
							tmp.transactions[0]=coinbase_txn
						else:
							tmp.transactions[i]=self.transactions[i-1]
					tmp.transactions.append(self.transactions[-1])
					self.transactions=tmp.transactions
			else:
				self.transactions.append(coinbase(MINING_ADDR, BLOCK_REWARD))
			work=self.as_bytes()
			target=diff2target(self.diff_bits)
			start = millis()
			begin = start
			hashes = 0
			for nonce in range(max_nonce):
				hashes += 1
				if (millis() - start >= 60000):
					log.info("Mining at {} h/s".format( hashes/((millis()-start)/1000)))
					start = millis()
					hashes = 0
				# increment the nonce
				self.nonce=nonce
				work=self.as_bytes()

				# hash the block
				hash_result=make_hash(work)
#				print("hash={} nonce={} value={} target={}".format(hash_result, nonce, int(hash_result, 16), target))
            	# check if this is a valid result, below the target
				if (check_diff(self.diff_bits, hash_result) == True):
					#  set the hash of self to the hash we found
					self.hash=str(hash_result)
					if nonce > 0 and millis()-begin > 0:
						log.info("Avg. hashrate={} h/s".format( nonce/((millis()-begin)/1000)))
					return None

	def as_bytes(self):
		out="{}{}{}{}{}{}{}".format(self.height, self.diff_bits, self.timestamp,
		                            self.nonce, self.transactions, self.version, self.prev_hash)
		return out
	def valid(self):
		if self.hash == '':  # a hash should never be blank
			return 'empty hash'
		else:
			tmp=self  # clonse self into a temp block buffer
			tmp.hash()  # hash the temp block buffer
			if (tmp.hash != self.hash):  # if the temp block resultant hash is not that of self.hash return err
				return 'bad block hash'
		if (self.height < 0):  # check nonce is postive
			return 'negative nonce'
		else:
			tmp=Block()  # create shell block
			# try to read the block with hash self.prev_hash into the shell block
			read_err=tmp.get(hash=self.prev_hash)
			if (read_err != None):  # if it failed return
				return 'failed to read prev block. error='+read_err
			# if the read block's height is not 1 behind self.height return err'
			elif (tmp.height != self.height-1):
				return 'height missmatch'
		if (int(self.hash, 16) < self.diff_bits):  # check the diff bits and the hash match up
			return 'hash difficulty low'
		elif (False):  # todo: check if diff bits is over or equal to difficulty for height self.height
			return 'diff bits low'
		else:
			i=0
			for tx in self.transactions:
				i += 1 
				if (tx.valid() == False):
					return 'tx at slot=' + i + ' invalid'
		#if (sys.sizeof(self) > MAX_BLOCK_SIZE):  # TODO: check size of block
		#	return 'block too big'

	def hash_blk(self):
		work=self.as_bytes()
		self.hash=make_hash(work)
		return self.hash()
	def save(self):
		set('blk-{}'.format(self.height), self.to_json(), 'coofblocks')
		set(self.hash, str(self.height), 'coofblocksindex')
		return True

	def get(self, height=None, hash=None):
		if height == None and hash == None:
			return 'must provide either hash or height'
		elif height == None:
			# get using hash
			height=get(hash, 'coofblocksindex')
		as_json=get('blk-{}'.format(height), 'coofblocks')
		if as_json == None:
			return 'block not found'
		self.from_json(as_json)
		return self

def coinbase(miner, reward=BLOCK_REWARD):
		coinbase_input= txIn('', '', amount=reward,
		                    signature='', owner=miner, index=0)
		coinbase_input.hash_in()
		got = get('outputindex', 'coofchainstatus')
		if got == None:
			got = 0
		output_count=int(got) + 1
		set('outputindex', str(output_count),'coofchainstatus')
		out = txOut(hash='', index=output_count, owner=miner, amount=reward,allowed_infection=False, immune=False)
		out.hash_out()
		txn = Transaction(type=0, sender='coinbase', to=miner, inputs=[coinbase_input], outputs=[out])
		txn.hash_tx()
		return txn

def genesis(): # TODO: return same hardcoded block every time
		gen_blk = Block(timestamp=time.time()*1000, transactions=[])
		gen_blk.transactions.append(coinbase(GENESIS_REWARD_ADDR, PREMINE))
		gen_blk.mine(1)
		return gen_blk
