import urllib2
import logging

PDS_BASE = '/opt/PDS/'
DATA_FILE_LOCATION = '%s/distro_data' % PDS_BASE
LOG_FILE_LOCATION = '%s/log/pds.log' % PDS_BASE
MIN_DATA_FILE_SIZE = 50000
MAX_RECORDS_TO_CONCAT = 5000

proxy_user = 'proxy_user'
proxy_password = 'proxy_password'
proxy_server = 'proxy_server'
proxy_port = 'proxy_port'

enable_proxy_authentication = False
server_host = '0.0.0.0'
server_port = 5000

DISABLE_PAGINATION = False

'''
Following are the various debug levels:
CRITICAL
ERROR
WARNING
INFO
DEBUG
NOTSET
Refer https://docs.python.org/2/library/logging.html for more information.
'''
DEBUG_LEVEL = logging.ERROR

DISTROS_WITH_BIT_REP = {
    'Ubuntu': {
        'Ubuntu__17.04': 0,
        'Ubuntu__16.10': 0,
        'Ubuntu__16.04': 0,
    }, 'Suse_Linux_Enterprise_Server': {
        'Suse_Linux_Enterprise_Server__11_SP4': 0,
        'Suse_Linux_Enterprise_Server__12_SP1': 0,
        'Suse_Linux_Enterprise_Server__12_SP2': 0
    }
}

logging.basicConfig(format='%(asctime)s %(message)s', filename=LOG_FILE_LOCATION, level=DEBUG_LEVEL)

LOGGER = logging.getLogger('PDS_SERVER')

def generateDistroBitReps():
    bit_value = '1'
    for distro_type in DISTROS_WITH_BIT_REP:
        for distro in DISTROS_WITH_BIT_REP[distro_type]:
            DISTROS_WITH_BIT_REP[distro_type][distro] = int(bit_value, 2)
            bit_value += '0'

generateDistroBitReps()
# In case application is hosted on server with proxy, set "enable_proxy_authentication = True" in config.py 
# and update the proxy details
def proxy_authentication():
    proxy = urllib2.ProxyHandler({'http': 'http://%s:%s@%s:%s' % (proxy_user, proxy_password, proxy_server, proxy_port),
      'https': 'https://%s:%s@%s:%s' % (proxy_user, proxy_password, proxy_server, proxy_port)}
    )
    auth = urllib2.HTTPBasicAuthHandler()
    opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
