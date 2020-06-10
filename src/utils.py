from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import time as time_  # make sure we don't override time
import logging
import sys

class Wallet:
    balance = 0
    outputs = []
    pubkey = ''
    privkey = ''
    address = ''

    def __init(self, balance=0, outputs=[], pubkey='', privkey='', address=''):
        self.balance = balance
        self.outputs = outputs
        self.pubkey = pubkey
        self.privkey = privkey
        self.address = address

    def gen_keypair(self):
        self.privkey = Ed25519PrivateKey.generate()
        self.pubkey = self.privkey.public_key()
        self.address = self.pubkey.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ).hex()

# thanks to https://stackoverflow.com/a/6000198


def millis():
    return int(round(time_.time() * 1000))


def cal_average(num=[]):
    if len(num) == 1:
        return num[0]
    elif len(num) == 0:
        return 0
    else:
        sum_num = 0
        for t in num:
            sum_num = sum_num + t

        avg = sum_num / len(num)
        return avg

# Function to convert


def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1

def log_init(logPath='./', fileName='coof'):
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)

    fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)