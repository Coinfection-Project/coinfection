'''
 (c) 2020 Coinfection Project
 This code is licensed under the GNU General Public License v3.0 (see LICENSE.txt for details)
'''

from utils import *
from config import *
import math

''' 
Based of cryptonote specification #10
(https://cryptonote.org/cns/cns010.txt)
Thanks to the turtlecoin server for helping me out on understanding how to implement the following two
'''
# check a hashes diff 
def check_diff(diff, hash):
  return (int(hash, 16) * diff) < 2**256

# diff into target
def diff2target(diff):
 return math.floor((2**256 - 1) / diff)

# based on a simplifyed form of BTC's diff algo
def compute_difficulty(block, blockparent):
    if (block.timestamp < blockparent.timestamp):
        return 1
    return block.diff_bits * 20 / ((block.timestamp - blockparent.timestamp) / 1000)
    # *SHOULD* result in a approx time of 20 secconds per block, adjusts every block. 

def difficulty_test():
    from block import Block
    BLOCKCHAIN = []
    first = True
    wallet = Wallet()
    wallet.gen_keypair()
    set_mining_addr(wallet.address)
    while True:
        if (first == False):
            print("creating new block")
            pb = BLOCKCHAIN[-1]
            diff = 1
            if (len(BLOCKCHAIN) > 1):
                diff = compute_difficulty(pb, BLOCKCHAIN[-2])
            new_block = Block(height=pb.height+1, hash='', diff_bits=diff, timestamp=millis(), transactions=[], nonce=0, version=100, prev_hash=pb.hash)
            print("Created block, mining")
            new_block.mine(diff)
            print("Mined block. hash={} time={} (sec) difficulty={}".format(new_block.hash, (millis()-new_block.timestamp) / 1000, new_block.diff_bits))
            BLOCKCHAIN.append(new_block)
        else:
            print("creating genesis block")
            diff = 1
            new_block = Block(height=0, hash='', diff_bits=diff, timestamp=millis())
            print("Created genesis block, mining")
            new_block.mine(1)
            print("Mined genesis block. hash={} time={}(sec) difficulty={}".format(new_block.hash, (millis()-new_block.timestamp) / 1000, new_block.diff_bits))
            BLOCKCHAIN.append(new_block)
            first = False
            time.sleep(1) # to prevent diff adjust issues

                
