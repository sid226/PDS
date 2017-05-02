import urllib2
import logging


DATA_FILE_LOCATION = '/opt/PDS/src/distro_data'
LOG_FILE_LOCATION = '/opt/PDS/log/pds.log'
MIN_DATA_FILE_SIZE = 50000
MAX_RECORDS_TO_CONCAT = 5000

proxy_user = 'proxy_user'
proxy_password = 'proxy_password'
proxy_server = 'proxy_server'
proxy_port = 'proxy_port'

local_setup = False

enable_proxy_authentication = False
server_host = '0.0.0.0'
server_port = 5000

REPO_TYPE = 'external'

DISTROS = {
    "ubuntu": ("16.04", "16.10")
}

ARCHIVE_COPY_LIMIT = 2
DISABLE_PAGINATION = False

if local_setup:
    logging.basicConfig(format='%(asctime)s %(message)s', filename=LOG_FILE_LOCATION, level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)s %(message)s', filename=LOG_FILE_LOCATION, level=logging.ERROR)

LOGGER = logging.getLogger('PDS_SERVER')

# In case application is hosted on server with proxy, set "enable_proxy_authentication = True" in config.py 
# and update the proxy details
def proxy_authentication():
    proxy = urllib2.ProxyHandler({'http': 'http://%s:%s@%s:%s' % (proxy_user, proxy_password, proxy_server, proxy_port),
      'https': 'https://%s:%s@%s:%s' % (proxy_user, proxy_password, proxy_server, proxy_port)}
    )
    auth = urllib2.HTTPBasicAuthHandler()
    opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
