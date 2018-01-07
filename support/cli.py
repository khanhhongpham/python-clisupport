__author__ = 'KHANH'

import logging.config

import getpass
import sys
import json

from . import __version__, _support_data_path, _request_id
from cliargparser import CLIArgParser
from commands import CLICommand


SESSION = {'user_agent_name': getpass.getuser(), 'user_agent_version': __version__}

logging_config_json_file = open(_support_data_path + '/logging.json')
parsed_logging_data = json.load(logging_config_json_file)
# ajust format detail with requestid
parsed_logging_data['formatters']['detail']['format'] = """%(asctime)s - %(name)s - %(levelname)s - """ \
                                                        + str(_request_id) + """: \n%(message)s"""
logging.config.dictConfig(parsed_logging_data)
logger = logging.getLogger(__name__)

def main():
    session = CLISession(session=SESSION)
    return session.main()


class CLISession(object):
    def __init__(self, session=None):
        if session is None:
            self.session = SESSION
        else:
            self.session = session

    def main(self):
        """
        :param args: List of arguments, with the 'support' removed.
        """
        logger.debug(SESSION)
        parser = CLIArgParser()
        CLICommand(parser)


