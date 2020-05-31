GENESIS_REWARD_ADDR = '0x'  # the address which the premine goes to
NICKNAME_MAX_SIZE = 10  # in bytes
PREMINE = 0  # in singleton units
DECIMALS = 18  # the number of decimals
# the number of singletons that form a coin
SINGLETON_COLLECTION_AMOUNT = int('1' + ('0' * DECIMALS))
TICKER = 'COOF'  # the ticker of the coin (eg BTC, LTC, ETH)
# the name of the coin (lower case; eg bitcoin, litecoin, monero)
NAME = 'coinfect'
# the contract addr of the token addr that this coin can be swaped into
TOKEN_CONTRACT_ADDR = ''
BLOCK_TIME = 5 * 60  # the target time beetween blocks, in secconds
# the number of infection transactions a infectee can send per epoch (1 epoch = block time)
MAX_INFECTIONS_PER_EPOCH = 3
CLIENT_VERSON = 100  # the version of this software
# (50 COOF) the reward for mining one block, in singleton units
BLOCK_REWARD = 50000000000000000000
# (25 COOF) the reward for infecting someone, in singleton units
INFECTION_REWARD = 25000000000000000000
# (5 COOF) the reward, in singleton units, for being infected
INFECTED_REWARD = 5000000000000000000
RECOVERY_TIME = 50  # the number of epoches a infected node must be offline for for his coins to become recovered and immune
# the wallet addr of the wallet that starts as infected
PATIENT_ZERO = GENESIS_REWARD_ADDR
MINING_ADDR = ''  # the miners addr
# the number of tokns that a infection event infects, eg you have to have this many tokens to be able to be infected. For every TOKEN_INFECTION_CLUMP infected tokens you have you get MAX_INFECTIONS_PER_EPOCH infection transaction slots in the mempool
TOKEN_INFECTION_CLUMP = 100 * SINGLETON_COLLECTION_AMOUNT
# the number of transactions that can be in the mempool at anyone time
MEMPOOL_MAX_SLOTS = 32
# the minimum fee that a transaction must spend
TRANSACTION_MIN_FEE = 0.5 * SINGLETON_COLLECTION_AMOUNT
# the mimum bid for a nickname
NICKNAME_MIN_BID = 0.01 * SINGLETON_COLLECTION_AMOUNT
# the number of epoches (blocks) a nickname auction lasts
NICKNAME_AUCTION_EPOCH_PERIOD = 100
MAX_BLOCK_SIZE = 50000000  # (50Mb) the max size a block can be, in bytes

# funcs


def set_mining_addr(addr):
    MINING_ADDR = addr
