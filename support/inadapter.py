__author__ = 'KHANH'
import requests
import logging
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.ERROR)

class IN:
    def __init__(self, tenant):
        self.tenant = tenant

    def get_usage(self, phonenumber):
        url = 'http://example.com' + str(phonenumber)
        headers = {'Content-Type': 'application/json', 'X-IO-Partner-Id': 'example',
                   'X-IO-Tenant-Id': 'example', 'X-IO-RequestSource': 'internal'}
        res = requests.get(url, headers=headers, timeout=10)
        result = res.json()
        if res.status_code == 200:
            return result['carrierServicePlans']
        else:
            return result
