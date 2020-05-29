# Import the python libraries
import pymongo
import logging
from transaction import 
import mempool
log = logging.getLogger(__name__)

# Connect to client
client = pymongo.MongoClient("localhost", 27017)
log.info("Loading state db")
# Connect to the coinfection db 
db=client.coof_db
collection = db.mempool
# Read every saved transaction
cursor = collection.find({})
for document in cursor:
  txn = Transaction(**json.load(document))
  log.debug('Loaded transaction from db. hash={}'.format(txn.hash))
  if (txn.valid()):
    if (mempool.in_mempool(txn.hash) == False):
      MEMPOOL.push(txn)
      log.trace("loaded txn to mempool. hash={}".format(txn.hash)
