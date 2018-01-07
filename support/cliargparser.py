
import argparse
import sys
import logging

logger = logging.getLogger(__name__)


HELP = (
    "To see help text, you can run:\n"
    "\n"
    "  clisupport --help\n"
    "  clisupport <command> --help\n"
    "  clisupport sync_quota \n"
    "  clisupport usage \n"
)
USAGE = (
    "clisupport <command> [parameters]\n"
    "%s" % HELP
)


class CLIArgParser(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='cli tool for support',
            usage=USAGE)
        parser.add_argument('command')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            logger.info('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        self.command = args.command

        getattr(self, self.command)()

    def check_usage(self):
        parser = argparse.ArgumentParser('Check Usage example - IN E///')
        parser.add_argument('-l', '--list-number', type=lambda s: [int(item) for item in s.split(',')],
                            help='List number, separate by comma')
        parser.add_argument('-f', "--file", type=str, help="File of numbers")
        self.args = parser.parse_args(sys.argv[2:])

    def sync_quota(self):
        parser = argparse.ArgumentParser('Sync Quota example - IN E///')
        parser.add_argument('-l', '--list-number', type=lambda s: [int(item) for item in s.split(',')],
                            help='List number, separate by comma')
        parser.add_argument("-f", "--file", type=str, help="File of numbers")
        self.args = parser.parse_args(sys.argv[2:])




