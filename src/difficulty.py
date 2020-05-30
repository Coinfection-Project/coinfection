'''
 (c) 2020 Coinfection Project
 This code is licensed under the GNU General Public License v3.0 (see LICENSE.txt for details)
'''

'''
Homestead eth pow difficulty algo
Thanks to eth and https://github.com/giact/ for this diff algo
https://github.com/giact/ethereum-blocktime-simulator/blob/master/ethereum-blocktime-simulator.py
'''
from block import *
import time
from wallet_utils import *
from config import *

def compute_difficulty(block, blockparent):
    d0 = 131072  # difficulty floor as defined by the protocol
    x = blockparent.diff_bits / 2048
    if block.timestamp <= blockparent.timestamp:
        return d0
    else:
        # current protocol
        sigma = max(1 - (block.timestamp - blockparent.timestamp) / 10, -99)
    return max(d0, blockparent.diff_bits + sigma * x)

def difficulty_test():
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
            new_block = Block(height=pb.height+1, hash='', diff_bits=diff, timestamp=time.time()*1000, transactions=[], nonce=0, version=100, prev_hash=pb.hash)
            print("Created block, mining")
            new_block.mine(diff)
            print("Mined block. hash={} time={} difficulty={}".format(new_block.hash, (time.time()*1000)-new_block.timestamp, new_block.diff_bits))
            BLOCKCHAIN.append(new_block)
        else:
            print("creating genesis block")
            diff = 1
            new_block = Block(height=0, hash='', diff_bits=diff, timestamp=time.time()*1000)
            print("Created genesis block, mining")
            new_block.mine(1)
            print("Mined genesis block. hash={} time={} difficulty={}".format(new_block.hash, (time.time()*1000)-new_block.timestamp, new_block.diff_bits))
            BLOCKCHAIN.append(new_block)
            first = False
            time.sleep(1) # to prevent diff adjust issues

                
