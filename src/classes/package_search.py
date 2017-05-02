import json
import os
import urllib
import collections
from sets import Set
from config import DATA_FILE_LOCATION, DISABLE_PAGINATION, MAX_RECORDS_TO_CONCAT, LOGGER

class PackageSearch:
    package_data = {}
    supported_distros = {}
    INSTANCE = None

    # Load all distro data
    distro_bit_mapping = {
        'UBUNTU_17.04': '0',
        'UBUNTU_16.10': '0',
        'UBUNTU_16.04': '0',
        'SUSE_LINUX_ENTERPRISE_SERVER_12-SP2': '0',
        'SUSE_LINUX_ENTERPRISE_SERVER_12-SP1': '0',
        'SUSE_LINUX_ENTERPRISE_SERVER_11-SP4': '0'
    }

    @classmethod
    def getDistroBitRepData(cls, bit_array):
        return_string_order = ('UBUNTU_17.04', 'UBUNTU_16.10', 'UBUNTU_16.04', 'SUSE_LINUX_ENTERPRISE_SERVER_12-SP2', \
                               'SUSE_LINUX_ENTERPRISE_SERVER_12-SP1', 'SUSE_LINUX_ENTERPRISE_SERVER_11-SP4'
                               )

        return_string = ''
        for i in return_string_order:
            return_string += bit_array[i]
        return return_string

    @classmethod
    def getDataFilePath(cls):
        '''This method will resolve the distributions data path based on configuration file to give actual 
        location of the file.
        '''
        LOGGER.debug('In getDataFilePath')
        return DATA_FILE_LOCATION

    def getSupportedDistros(self):
        LOGGER.debug('In getSupportedDistros')
        if self.supported_distros:
            return self.supported_distros
        else:
            return self.loadSupportedDistros()

    @classmethod
    def loadSupportedDistros(cls):
        '''
        Returns list of supported OS distributions in PDS
        '''

        LOGGER.debug('loadSupportedDistros: In loadSupportedDistros')

        json_data = []
        try:
            distro_data_file = '%s/distros_supported.json' % cls.getDataFilePath()
            json_data = json.load(open(distro_data_file))
        except Exception,ex:
            LOGGER.warn('loadSupportedDistros: In loadSupportedDistros %s distro loading resulted in: %s' % (distro_data_file, str(ex)))
        return json_data

    @classmethod
    def get_instance(cls):
        LOGGER.debug('get_instance: In get_instance')
        if not cls.INSTANCE:
            cls.INSTANCE = PackageSearch()
            cls.INSTANCE.supported_distros = cls.loadSupportedDistros()
            cls.INSTANCE.package_data = cls.loadPackageData()
            LOGGER.debug('get_instance: Creating singleton instance in get_instance')
        return cls.INSTANCE

    @classmethod
    def load(cls):
        LOGGER.debug('In load')
        return cls.get_instance()

    @classmethod
    def loadPackageData(cls):
        '''
        Returns list of Packages in PDS
        '''

        LOGGER.debug('loadPackageData: In loadSupportedDistros')
        distro_data_file = '%s/cached_data.json' % cls.getDataFilePath()
        try:
            json_data = json.load(open(distro_data_file))           
        except:
            LOGGER.warn('loadPackageData: Loading cached distros data failed generating from scratch')
            LOGGER.debug('loadPackageData: start writing distros data')
            json_data = cls.preparePackageData()
            cached_file = open(distro_data_file, 'w')
            cached_file.write(json_data)
            cached_file.close()
            LOGGER.debug('loadPackageData: end writing distros data')

        LOGGER.debug('loadPackageData: Loading supported distros data')

        return json_data

    def getPackagesFromURL(self, package_name, exact_match, page_number, page_size, sort_key = 'name', reverse = False, distro_bit_search_mapping_vals = '0'):
        '''
        This API will try to read from JSON files for various distros 
        and return the filtered set of results based on given search 
        keywords and distros to search from.
        '''
        LOGGER.debug('getPackagesFromURL: In function')
        package_name = urllib.unquote(package_name)

        LOGGER.debug('getPackagesFromURL: package_name figured out: %s', package_name)

        LOGGER.debug('getPackagesFromURL: bit rep generated : %s', distro_bit_search_mapping_vals)

        actual_package_name = package_name.replace('*', '');

        if exact_match:
            matches_based_on_package_name = filter(lambda s: s['packageName'] and s['packageName'] == actual_package_name, self.INSTANCE.package_data)
        elif ((str(package_name).startswith('*') and str(package_name).endswith('*')) or '*' not in str(package_name)):
            matches_based_on_package_name = filter(lambda s: s['packageName'] and actual_package_name in s['packageName'], self.INSTANCE.package_data)
        elif str(package_name).endswith('*'):
            matches_based_on_package_name = filter(lambda s: s['packageName'] and str(s['packageName']).startswith(actual_package_name), self.INSTANCE.package_data)
        elif str(package_name).startswith('*'):
            matches_based_on_package_name = filter(lambda s: s['packageName'] and str(s['packageName']).endswith(actual_package_name), self.INSTANCE.package_data)

        LOGGER.debug('getPackagesFromURL: Search on package name : %s', len(matches_based_on_package_name))

        matches_based_on_search = filter(lambda s: ((s['bit_rep_dec'] & distro_bit_search_mapping_vals) > 0), matches_based_on_package_name)

        LOGGER.debug('getPackagesFromURL: Search on bit rep : %s', len(matches_based_on_search))

        matches_based_on_search = sorted(matches_based_on_search, key = lambda k:k['packageName'], reverse = reverse)
        LOGGER.debug('getPackagesFromURL: Sorting done')

        if DISABLE_PAGINATION:
            start = 0
            end = len(matches_based_on_search)
        elif page_number:
            start = (page_number*page_size) - page_size
            end = (page_number*page_size)
        else:
            start = 0
            end = page_size

        LOGGER.debug('getPackagesFromURL: Applied pagination changes')

        final_data = {
            'total_packages': len(matches_based_on_search),
            'packages': matches_based_on_search[start: end]
        }

        LOGGER.debug('getPackagesFromURL: Sending final data to calling function')

        LOGGER.debug(final_data)        

        return json.dumps(final_data)

    @classmethod
    def preparePackageData(cls):
        data_dir = cls.getDataFilePath()
        package_info = [];
        package_data = {};
        for distro_file in os.listdir(data_dir):
            if not distro_file.startswith('distros_supported') and distro_file != 'cached_data.json':
                package_info = json.load(open('%s/%s' % (data_dir, distro_file)))
                distro_file_name = distro_file                  
                distro_info = distro_file_name.replace('_Package_List.json', '')
                
                distro_info = distro_info.split('_')
                if len(distro_info) > 1:
                    distro_name = distro_info[0]
                    distro_version = distro_info[1:len(distro_info)]
                    if distro_name.startswith('SUSE'):
                        distro_name = '_'.join(distro_info[0:4])
                        distro_version = distro_info[4:len(distro_info)]
                        distro_version = '-'.join(distro_version)
                    else:
                        distro_version = '.'.join(distro_version)

            for pkg in package_info:
                try:
                    pkg_key = pkg["packageName"] + '_' + pkg["version"]
                except Exception as ex:
                    LOGGER.error('preparePackageData: key not found for package %s' % str(ex))
                if not package_data.has_key(pkg_key):
                    pkg[distro_name] = [distro_version]
                    package_data[pkg_key] = pkg
                else:
                    if not package_data[pkg_key].has_key(distro_name):
                        package_data[pkg_key][distro_name] = [distro_version]
                    else:
                        if distro_version not in package_data[pkg_key][distro_name]:
                            package_data[pkg_key][distro_name].append(distro_version)

        json_data = package_data.values()

        return cls.generateBitDataForPackages(json_data)

    @classmethod
    def generateBitDataForPackages(cls, json_data):
        for item in json_data:
            distros = filter(lambda elem: elem != 'packageName' and elem != 'version' and elem != 'url', item.keys())

            for i in range(0, len(distros)):
                distro_versions = item[distros[i]]
                for j in range(0, len(distro_versions)):
                    cls.distro_bit_mapping[distros[i] + '_' + distro_versions[j]] = '1'

            values = cls.getDistroBitRepData(cls.distro_bit_mapping)
            LOGGER.debug(cls.distro_bit_mapping)

            item['bit_rep_dec'] = int(''.join(values),2)
            item.pop('url',None)

            cls.distro_bit_mapping = {
                'UBUNTU_17.04': '0',
                'UBUNTU_16.10': '0',
                'UBUNTU_16.04': '0',
                'SUSE_LINUX_ENTERPRISE_SERVER_12-SP2': '0',
                'SUSE_LINUX_ENTERPRISE_SERVER_12-SP1': '0',
                'SUSE_LINUX_ENTERPRISE_SERVER_11-SP4': '0'
            }

        return json.dumps(json_data)