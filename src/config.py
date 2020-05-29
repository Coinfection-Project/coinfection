GENESIS_REWARD_ADDR = '0x' # the address which the premine goes to
NICKNAME_MAX_SIZE = 10 # in bytes
PREMINE = 0 # in singleton units
DECIMALS = 18 # the number of decimals
SINGLETON_COLLECTION_AMOUNT = int('1' + ('0' * DECIMALS)) # the number of singletons that form a coin
TICKER = 'COOF' # the ticker of the coin (eg BTC, LTC, ETH)
NAME = 'coinfect' # the name of the coin (lower case; eg bitcoin, litecoin, monero)
TOKEN_CONTRACT_ADDR = '' # the contract addr of the token addr that this coin can be swaped into
BLOCK_TIME = 5 * 60 # the target time beetween blocks, in secconds
MAX_INFECTIONS_PER_EPOCH = 3 # the number of infection transactions a infectee can send per epoch (1 epoch = block time)
CLIENT_VERSON = 100 # the version of this software
BLOCK_REWARD  = 50000000000000000000 # (50 COOF) the reward for mining one block, in singleton units
INFECTION_REWARD = 25000000000000000000 # (25 COOF) the reward for infecting someone, in singleton units
INFECTED_REWARD = 5000000000000000000 # (5 COOF) the reward, in singleton units, for being infected
RECOVERY_TIME = 50 #  the number of epoches a infected node must be offline for for his coins to become recovered and immune
PATIENT_ZERO = GENESIS_REWARD_ADDR # the wallet addr of the wallet that starts as infected
MINING_ADDR = '' # the miners addr
TOKEN_INFECTION_CLUMP = 100 * SINGLETONS_COLLECTION_AMOUNT # the number of tokns that a infection event infects, eg you have to have this many tokens to be able to be infected. For every TOKEN_INFECTION_CLUMP infected tokens you have you get MAX_INFECTIONS_PER_EPOCH infection transaction slots in the mempool
MEMPOOL_MAX_SLOTS = 32 # the number of transactions that can be in the mempool at anyone time
TRANSACTION_MIN_FEE = 0.5 * SINGLETON_COLLECTION_AMOUNT # the minimum fee that a transaction must spend
NICKNAME_MIN_BID = 0.01 * SINGLETON_COLLECTION_AMOUNT #  the mimum bid for a nickname
NICKNAME_AUCTION_EPOCH_PERIOD = 100 # the number of epoches (blocks) a nickname auction lasts
MAX_BLOCK_SIZE = 50000000 # (50Mb) the max size a block can be, in bytes

# funcs
def set_mining_addr(addr):
	MINING_ADDR = addr
