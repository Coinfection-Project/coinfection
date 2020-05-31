'''
 (c) 2020 Coinfection Project
 This code is licensed under the GNU General Public License v3.0 (see LICENSE.txt for details)
'''
from db import set, get
from block import Block, genesis

TOP_BLOCK = None

read_block_height = get('height', 'coofchainstatus')
if read_block_height == None:
  # save the genesis block
  genesis = genesis()
  print("No blocks found, saving geneis block to db")
  genesis.save()
  set('height', '0', 'coofchainstatus')
  TOP_BLOCK = genesis

def get_block_height():
  return TOP_BLOCK.height

def set_top_block(new):
  TOP_BLOCK = new
  set('height', str(new.height), 'coofchainstatus')
  return True
  
def top_block():
  return TOP_BLOCK

def get_block(height):
  return get("blk-{}".format(height), 'coofblocks')
