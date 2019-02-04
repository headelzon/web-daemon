#!/usr/bin/env python

import sys
import os
import logging
import argparse

from daemon import Daemon
from core import main
from mailer import Mailer


class MyDaemon(Daemon):
    def _run(self):
        main(self.logger, self.path, url, email, frequency)


def setup(logs=False):
    logger.info('Clearing resources and logs')
    folders = ['./resources']

    if logs:
        folders.append('./logs')

    for folder in folders:
        for f in os.listdir(folder):
            file_path = os.path.join(folder, f)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)

            except Exception as e:
                logger.error("Error clearing resources/logs: " + e.__str__())


path = os.getcwd()

logger = logging.getLogger('web-daemon')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(path + '/logs/daemon-logs.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s -- %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

frequency = None
url = None
email = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('mode', choices=['start', 'stop', 'restart', 'clear'],  help='Running mode')
    parser.add_argument('-a', '--address', help='Website url')
    parser.add_argument('-e', '--email', help='Email address to send notifications to')
    parser.add_argument('-f', '--frequency', type=int, help='Frequency of website check in seconds (30 - 86400)')

    args = parser.parse_args()

    if args.mode == 'start':
        if not args.email:
            print('You must include your email!')
            parser.print_help()
            sys.exit(2)
        if not args.address:
            print('You must include a web address to monitor!')
            parser.print_help()
            sys.exit(2)

    email = args.email
    daemon = MyDaemon(path, path + '/tmp/web-daemon.pid', logger)

    if args.mode == 'start':
        frequency = args.frequency
        url = args.address
        setup()
        daemon.start()
    elif args.mode == 'stop':
        daemon.stop()
    elif args.mode == 'restart':
        daemon.restart()
    elif args.mode == 'clear':
        setup(logs=True)

    sys.exit(0)

