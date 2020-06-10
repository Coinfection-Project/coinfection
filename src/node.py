from utils import log_init
from db import init_db, get, set
import logging
from difficulty import *
import node_api as api
def launch():
    log = logging.getLogger(__name__)
    log_init('./', 'coof')
    log.info("Connecting to db")
    init_db()
    log.info("Connected to db")
    log.info("Launching api")
    api.launch()
    log.info('Starting difficulty test')
    difficulty_test()
    log.info("finished diff test")

if __name__ == "__main__":
    launch()