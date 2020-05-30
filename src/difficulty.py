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

def compute_difficulty(block, blockparent):
    d0 = 131072  # difficulty floor as defined by the protocol
    x = blockparent.difficulty / 2048
    if block.timestamp <= blockparent.timestamp:  # protocol demands a strictly increasing timestamp
        raise ValueError(
            "Timestamp must always increase (blockparent: %d; currentblock: %d)" % (blockparent.timestamp, block.timestamp)
        )
    else:
        # current protocol
        sigma = max(1 - (block.timestamp - blockparent.timestamp) / 10, -99)
    return max(d0, blockparent.difficulty + sigma * x)

def difficulty_test():
    BLOCKCHAIN = []
    first = True
    while True:
        if (first == False):
            print("creating new block")
            pb = BLOCKCHAIN[-1]
            diff = 1
            if (len(BLOCKCHAIN) > 1):
                diff = compute_difficulty(pb, BLOCKCHAIN[-2])
            new_block = Block(height=pb.height+1, hash='', diff_bits=diff, timestamp=time.time()*1000, transactions=[], nonce=0, version=100, prev_hash=pb.hash)
            print("Created block, mining")
            new_block.mine()
            print("Mined block. hash={} time={} difficulty={}".format(new_block.hash, (time.now()*1000)-new_block.time, new_block.diff_bits))
            BLOCKCHAIN.push(new_block)
        else:
            print("creating genesis block")
            diff = 1
            new_block = Block(height=0, hash='', diff_bits=diff, timestamp=time.time()*1000)
            print("Created genesis block, mining")
            new_block.mine()
            print("Mined genesis block. hash={} time={} difficulty={}".format(new_block.hash, (time.now()*1000)-new_block.time, new_block.diff_bits))
            BLOCKCHAIN.push(new_block)
            first = False

                
