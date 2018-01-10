from os.path import basename
from os.path import dirname, abspath

_support_path = dirname(dirname(abspath(__file__)))
print _support_path
print basename(__file__)

