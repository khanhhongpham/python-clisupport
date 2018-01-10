__author__ = 'KHANH'
import uuid
from os.path import join, dirname, abspath

__version__ = '1.0.0'

_support_path = dirname(dirname(abspath(__file__)))
_support_data_path = join(dirname(dirname(abspath(__file__))), 'data')

_support_remote_output_path = '/mnt/ops/outgoing'
_request_id = uuid.uuid4()

