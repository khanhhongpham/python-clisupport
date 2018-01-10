__author__ = 'KHANH'
import requests
import time
import logging
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

policy_type_number = {'VOICE': 1, 'DATA': 2, 'MESSAGING': 3}


class UMS:
    def __init__(self, tenant):
        self.tenant = tenant

    def resync_usage(self, snid, policytype):
        time.sleep(2)
        url = 'http://example' \
              + snid + '/policy/' + str(policy_type_number[policytype])
        headers = {'Content-Type': 'application/json',
                   'X-IO-Tenant-Id': 'example', 'X-IO-RequestSource': 'internal'}
	logger.debug("Calling: %s %s" % (url, headers))
        res = requests.post(url, headers=headers, timeout=10)
        result = res.json()
        return result
