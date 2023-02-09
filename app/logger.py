import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('log.log')
format = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(format)

logger.addHandler(handler)

