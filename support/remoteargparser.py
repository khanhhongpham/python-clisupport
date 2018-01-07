__author__ = 'KHANH'

import argparse
import sys
import logging

logger = logging.getLogger(__name__)



class RemoteArgParser(object):

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            logger.info('Unrecognized command')
            #parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        self.command = args.command
        # arguments
        self.args = []
        getattr(self, self.command)()

    def check_usage(self):
        parser = argparse.ArgumentParser(
            description='Check Usage example - IN E///',
            usage="""remotesupport check_usage -f <input file>""")
        parser.add_argument('-l', '--list-number', type=lambda s: [int(item) for item in s.split(',')],
                            help='List number')
        parser.add_argument("-f", "--file", type=str, help="File name", required=True)
        self.args = parser.parse_args(sys.argv[2:])

    def sync_quota(self):
        parser = argparse.ArgumentParser(
            description='Sync Quota tool example - IN E///',
            usage="""remotesupport sync_quota -f <input file>""")
        parser.add_argument('-l', '--list-number', type=lambda s: [int(item) for item in s.split(',')],
                            help='List number')
        parser.add_argument("-f", "--file", type=str, help="File name", required=True)
        self.args = parser.parse_args(sys.argv[2:])



