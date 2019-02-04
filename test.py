from core import main
import logging
import os


path = os.getcwd()

logger = logging.getLogger('web-daemon')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(path + '/logs/daemon-logs.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s -- %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
main(logger, path, "https://google.com", "wfkoziak@gmail.com")
