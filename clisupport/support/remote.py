__author__ = 'KHANH'

import logging.config

import json

from . import __version__,  _support_path, _support_data_path, _support_remote_output_path, _request_id
from remoteargparser import RemoteArgParser
from commands import CLICommand
from os.path import basename
from os import chdir
SESSION = {'user_agent_name': 'remote', 'user_agent_version': __version__}

logging_config_json_file = open(_support_data_path + '/logging.json')
parsed_logging_data = json.load(logging_config_json_file)
# ajust format detail with requestid
parsed_logging_data['formatters']['detail']['format'] = """%(asctime)s - %(name)s - %(levelname)s - """ \
                                                        + str(_request_id) + """: \n%(message)s"""


def main():
    session = RemoteSession(session=SESSION)
    return session.main()


class RemoteSession(object):
    def __init__(self, session=None):
        if session is None:
            self.session = SESSION
        else:
            self.session = session

    def main(self):
        chdir(_support_path)
        parser = RemoteArgParser()
        if parser.args.file is not None:
            output_filep = _support_remote_output_path + '/processed_' + basename(parser.args.file)
            parsed_logging_data['handlers']['console'] = {"class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": output_filep,
            "mode": "w",
            "encoding": "utf8"}
            logging.config.dictConfig(parsed_logging_data)
            logger = logging.getLogger(__name__)
            logger.debug(SESSION)
        count = 0
        with open(parser.args.file, 'rb') as f:
            for line in f:
                count += 1
        if count < 50:
            CLICommand(parser)
        else:
            logger.info("Input file shouldn't have more than 50 lines")


