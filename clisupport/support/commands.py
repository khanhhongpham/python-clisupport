__author__ = 'KHANH'

from functions import check_quota_in, sync_quota_in, check_quota_in_file, sync_quota_in_file


class CLICommand(object):

    """Interface for a CLI command.
    """
    def __init__(self, parser):
        # commands
        self.command = parser.command
        # arguments
        self.args = parser.args
        getattr(self, self.command)()

    def check_usage(self):
        if self.args.list_number is not None:
            check_quota_in(self.args.list_number)
        if self.args.file is not None:
            check_quota_in_file(self.args.file)
    def sync_quota(self):
        if self.args.list_number is not None:
            sync_quota_in(self.args.list_number)
        if self.args.file is not None:
            sync_quota_in_file(self.args.file)


