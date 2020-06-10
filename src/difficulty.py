'''
 (c) 2020 Coinfection Project
 This code is licensed under the GNU General Public License v3.0 (see LICENSE.txt for details)
'''

from utils import *
from config import *
import math
from time import sleep
import logging

log = logging.getLogger("diff test")

''' 
Based of cryptonote specification #10
(https://cryptonote.org/cns/cns010.txt)
Thanks to the turtlecoin server for helping me out on understanding how to implement the following three
'''
# check a hashes diff


def check_diff(diff, hash):
    return (int(hash, 16) * diff) < 2**256

# diff into target


def diff2target(diff):
    return math.floor((2**256 - 1) / diff)

# based on a simplifyed form of BTC's diff algo
# *SHOULD* result in a approx time of 20 secconds per block, adjusts every block.


def compute_difficulty(block):
    log.info("Calclating difficulty for block. hash={} height={} current_diff={}".format(block.hash, block.height, block.diff_bits))
    from block import Block
    # return a diff of 1 for the first 3 blocks
    if (block.height < 2):
        return 1
    deltas = []
    block_times = []
    if block.height < 60:
        for k in range(0, block.height):
            b = Block()  # init a shell block
            log.debug("Getting block at height={}".format(k))
            b.get(height=k)  # get block at height k
            if (k != 1):
                deltas.append(b.timestamp - block_times[-1])
            block_times.append(b.timestamp)
    else:
        for k in range(block.height-60, block.height):
            b = Block()  # init a shell block
            b.get(height=k)  # get block at height k
            if (k != 1):
                deltas.append(b.timestamp - block_times[-1])
            block_times.append(b.timestamp)
    log.debug("deltas: {}, times: {}".format(deltas, block_times))
    delta = cal_average(block_times)
    if (delta == 0):
        return block.diff_bits
    return block.diff_bits * 20 / (delta / 1000)


def difficulty_test():
    from block import Block, genesis
    from db import clear_db
    clear_db()
    BLOCKCHAIN = []
    first = True
    wallet = Wallet()
    wallet.gen_keypair()
    set_mining_addr(wallet.address)
    while True:
        if (first == False):
            log.info("creating new block")
            pb = BLOCKCHAIN[-1]
            diff = 1
            if (len(BLOCKCHAIN) > 1):
                diff = compute_difficulty(pb)
            new_block = Block(height=pb.height+1, hash='', diff_bits=diff, timestamp=millis(),
                              transactions=[], nonce=0, version=100, prev_hash=pb.hash)
            log.info("Created block, mining. diff={}".format(new_block.diff_bits))
            new_block.mine(diff)
            log.info("Mined block. hash={} time={} (sec) difficulty={}".format(
                new_block.hash, (millis()-new_block.timestamp) / 1000, new_block.diff_bits))
            BLOCKCHAIN.append(new_block)
        else:
            log.info("creating genesis block")
            diff = 1
            new_block = genesis()
            log.info("Created genesis block, mining")
            new_block.mine(1)
            log.info("Mined genesis block. hash={} time={}(sec) difficulty={}".format(
                new_block.hash, (millis()-new_block.timestamp) / 1000, new_block.diff_bits))
            BLOCKCHAIN.append(new_block)
            first = False
        new_block.save()
        sleep(1.5)  # to prevent diff adjust issues
