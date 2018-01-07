__author__ = 'KHANH'

import logging.config

import json

from . import __version__, _support_data_path, _request_id
import functions


SESSION = {'user_agent_name': 'integrator', 'user_agent_version': __version__}

logging_config_json_file = open(_support_data_path + '/logging.json')
parsed_logging_data = json.load(logging_config_json_file)
# ajust format detail with requestid
parsed_logging_data['formatters']['detail']['format'] = """%(asctime)s - %(name)s - %(levelname)s - """ \
                                                        + str(_request_id) + """: \n%(message)s"""
logging.config.dictConfig(parsed_logging_data)
logger = logging.getLogger(__name__)


def check_quota_in_dn(dn):
    logger.debug(SESSION)
    result = functions.check_quota_in_dn(dn)
    return result



