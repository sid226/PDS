# Adding new distributions to the tool

This documents details the steps to be performed in order to add a distribution support to PDS tool. 

_**General Notes:**_ 	

 * _A directory `/<DATA_FILE_LOCATION>/` defined in Step 6 of [Installation](Installation.md) document._

 * _A directory `/<PDS_BASE>/` defined in Step 6 of [Installation](Installation.md) document._

### Step 1. Create a JSON file with package data

All the distribution specific data files need to be added in the folder `<DATA_FILE_LOCATION>`. 

**The data file should be named in following convention in folder `<DATA_FILE_LOCATION>`:**

    <Distribution>_<Version>_Package_List.json

`<Distribution>` - Name of the distribution to be added for e.g. "Ubuntu"

_**Note:**_ 
In case distribution name contains spaces it should be replaced by '_'.

`<Version>` - Version of the distribution to be supported for e.g. 14.04

**Here's sample file naming:**

    Ubuntu_14.04_Package_List.json

The Content of the distribution data JSON file needs to be in format below:

```
[{
    "packageName": "<package_name_1>",
    "version": "<package_version_1>"
},{
    "packageName": "<package_name_2>",
    "version": "<package_version_2>"
},{
.
.
.
.
},{
    "packageName": "<package_name_n>",
    "version": "<package_version_n>"
}]
```

**Here's the sample data:**

```
[{
    "packageName": "ImageMagick-devel",
    "version": "6.4.3.6-7.20.1"
}, {
    "packageName": "KhmerOS-fonts",
    "version": "5.0-105.17"
}, {
    "packageName": "KhmerOS-fonts",
    "version": "5.0-105.17"
}, {
    "packageName": "LibVNCServer",
    "version": "0.9.1-156.1"
}]
```

### Step 2. Make an entry in the configuration file `/<PDS_BASE>/src/config/config.py` as below
The entry in the configuration file is to help generate a cache file `<DATA_FILE_LOCATION>/cached_data.json` which will be then loaded by the server while starting and used for processing requests.

```diff
@@ -39,6 +39,8 @@ DistributionS_WITH_BIT_REP = {
         'Suse_Linux_Enterprise_Server__11_SP4': 0,
         'Suse_Linux_Enterprise_Server__12_SP1': 0,
         'Suse_Linux_Enterprise_Server__12_SP2': 0
+    }, '<Distribution>': {
+        '<Distribution>__<Version>': 0
     }
 }
```
`<Distribution>` - Name of the distribution to be added for e.g. "Ubuntu"

_**Note:**_ 
In case distribution name contains spaces it should be replaced by '_'.

`<Version>` - Version of the distribution to be supported for e.g. 14.04

### Step 3. Delete the cached data file `<DATA_FILE_LOCATION>/cached_data.json`
The system needs to regenerate the cached_data after adding a new distro.  Hence delete the existing cache as follows:

```
cd <DATA_FILE_LOCATION>
rm -f cached_data.json
```

Restart the server by refering to the steps mentioned in [Installation](Installation.md) document.

