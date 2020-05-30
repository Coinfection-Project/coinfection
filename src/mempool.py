'''
(c) 2020 Coinfection Project
This code is licensed under the GNU General Public License v3.0 (see LICENSE.txt for details)
mempool.py handles the mempool, the place where unconfirmed transactions sit waiting to be added to a block
'''
# This is the global var in which unconfimed txns are stored
MEMPOOL = []

def in_mempool(txn_hash):
  for txn in MEMPOOL:
    if (txn.hash == txn_hash):
      return True
  return False;

def remove_from_mempool(txn_hash):
  i = 0
  for i in range(len(MEMPOOL)):
    if (MEMPOOL[i].__dict__['hash'] == txn_hash):
      MEMPOOL.pop(i)
      return True
  return False

def add_to_mempool(txn):
  if (in_mempool(txn.hash)):
    return False
  else:
    MEMPOOL.push(txn)
    return True

def add_to_mempool_no_check(txn):
  MEMPOOL.push(txn)
  return True

