'''
 (c) 2020 Coinfection Project
 This code is licensed under the GNU General Public License v3.0 (see LICENSE.txt for details)
'''

'''
Homestead eth pow difficulty algo
Thanks to eth and https://github.com/giact/ for this diff algo
https://github.com/giact/ethereum-blocktime-simulator/blob/master/ethereum-blocktime-simulator.py
'''
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
