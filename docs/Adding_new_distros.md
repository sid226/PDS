# Adding new distributions to the tool:

For adding any distribution following steps needs to be followed:

### 1. Add an entry in file `/opt/PDS/src/distro_data/distros_supported.json` as below:
```diff
@@ -4,6 +4,9 @@
 },{
     "name" : "Debian",
     "versions" : [ "8.0"]
+},{
+    "name" : "<distro_name>",
+    "versions" : [ "<distro_version>"]
 }, {
     "name" : "SUSE Linux Enterprise Server",
     "versions" : [ "12 SP2", "12 SP1", "11 SP4"]
```
`<distro_name>` - is the name of new distribution to be added.

`<distro_version>` - is the distribution version.

### 2. Add data of available packages in JSON format, for the distribution, in below format:
```
[{
    "packageName": "<package_name_1>",
    "updateVersion": "<latest_version_1>"
},{
    "packageName": "<package_name_2>",
    "updateVersion": "<latest_version_2>"
},{
.
.
.
.
},{
    "packageName": "<package_name_n>",
    "updateVersion": "<latest_version_n>"
}]
```

**Here's the sample data:**

```
[{
    "packageName": "ImageMagick-devel",
    "updateVersion": "6.4.3.6-7.20.1"
}, {
    "packageName": "KhmerOS-fonts",
    "updateVersion": "5.0-105.17"
}, {
    "packageName": "KhmerOS-fonts",
    "updateVersion": "5.0-105.17"
}, {
    "packageName": "LibVNCServer",
    "updateVersion": "0.9.1-156.1"
}]
```

**The data file above should be named in following convention in folder `/opt/PDS/src/distro_data/`:**

    <distro_name>_<distro_version>_Package_List.json

`<distro_name>` - is distribution name in upper case.

`<distro_version_1>` - is the distribution version that gets added.

**Here's sample file naming:**

    SUSE_LINUX_ENTERPRISE_SERVER_11_SP4_Package_List.json
