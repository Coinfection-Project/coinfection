# Import the python libraries
from hash import fast_hash
import pymongo
import logging
import mempool
import json

log = logging.getLogger(__name__)
db = None
def init_db():
    # Connect to client
    client = pymongo.MongoClient("localhost", 27017)
    log.info("Loading state db")
    # Connect to the coinfection db
    global db 
    db = client.coof_db
    collection = db.mempool
    # Read every saved unconfirmed transaction
    cursor = collection.find({})
    for document in cursor:
        import transaction
        txn = transaction.Transaction(**json.load(document))
        log.debug('Loaded transaction from db. hash={}'.format(txn.hash))
        if (txn.valid()):
            # revalidate it
            if (mempool.in_mempool(txn.hash) == False):
                # if it is not already loaded then load it
                mempool.MEMPOOL.append(txn)
                log.trace("loaded txn to mempool. hash={}".format(txn.hash))
            else:
                log.trace(
                    "Ignoring txn, already in mempool. hash={}".format(txn.hash))
        else:
            log.trace(
                "Loaded invalid unconfirmed txn, discarding. hash={}".format(txn.hash))
    return True

def get(key, collection_name):
    collection = db[collection_name]
    key = fast_hash(key)
    doc = collection.find_one({"_id": "{}".format(key)})
    if (doc != None):
        data = collection.find_one({"_id": "{}".format(key)})["data"]
        return data
    else:
        return None


def set(key, value, collection_name):
    collection = db[collection_name]
    key = fast_hash(key)
    if (collection.find_one({"_id": "{}".format(key)}) != None):
        myquery = {"_id": "{}".format(key) }
        newvalues = { "$set": {"_id": "{}".format(key), "data": "{}".format(value) } } 
        collection.update_one(myquery, newvalues)
        return True
    else:
        collection.insert_one(
            {"_id": "{}".format(key), "data": "{}".format(value)})
        return True


def list_all_items():
    collist = db.list_collection_names()
    for col in collist:
        print("Collection: {}".format(col))
        collection = db[col]
        cursor = collection.find({})
        for document in cursor:
            print(" - Doc: {}".format(document))

def clear_db():
    collist = db.list_collection_names()
    for col in collist:
        print("Collection: {}".format(col))
        collection = db[col]
        cursor = collection.find({})
        for document in cursor:
            collection.delete_one(document)
