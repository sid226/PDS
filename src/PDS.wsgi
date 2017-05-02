import sys

sys.path.append('/opt/PDS/src/')

from main import app as application
from config import local_setup, server_host, server_port
from classes import PackageSearch

package_search = PackageSearch()