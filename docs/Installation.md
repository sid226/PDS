# Steps for setting up PDS application on server

### Step 1: Install pre-requisite dependencies
Note: make sure you are logged in as user with sudo permissions

* RHEL:

        sudo yum install -y python python-setuptools gcc git libffi-devel python-devel openssl openssl-devel cronie apache2
        sudo easy_install pip

* SLES:

        sudo zypper install -y python python-setuptools gcc git libffi-devel python-devel openssl openssl-devel cronie python-xml pyxml apache2 aaa_base apache2-devel tar wget apache2-worker
        sudo easy_install pip

* Ubuntu:

        sudo apt-get update
        sudo apt-get install -y python python-pip gcc git python-dev libssl-dev libffi-dev cron python-lxml apache2

**Note:** if "/usr/local/bin" is not part of $PATH add it to the path:

        echo $PATH
        export PATH=/usr/local/bin:$PATH
        sudo sh -c "echo 'export PATH=/usr/local/bin:$PATH' > /etc/profile.d/alternate_install_path.sh"

### Step 2: Install Python dependencies libraries

        sudo pip install 'cryptography==1.4' Flask launchpadlib simplejson logging


###  Step 3: Checkout the code-base from gitlab, into /opt/ folder

        cd /opt/
        sudo git clone https://github.com/linux-on-ibm-z/PDS.git
        cd PDS

Note: In case PDS code is already checked out, but there is a new update to be fetched from repository, it should be updated as

        cd /opt/PDS
        sudo git pull origin master

###  Step 4: Set Environment variables
            
        sudo sh -c "echo 'export PYTHONPATH=/opt/PDS/src/classes:/opt/PDS/src/config:$PYTHONPATH' > /etc/profile.d/pds.sh"

###  Step 5: Copy the init.d script to start/stop/restart PDS application
        sudo chmod 755 -R /opt/PDS/src/setup
        cd /opt/PDS/src/setup
        sudo ./create_initid_script.sh

###  Step 6: Enable pds service
* RHEL:

        sudo systemctl reload pds

* SLES:

        sudo systemctl reload pds

* Ubuntu:

        sudo initctl reload-configuration

        
###  Step 7: Start the Flask server as below

        sudo service pds start

###  Step 8: Verify that the server is up, by running the application in browser
        http://server_ip_or_fully_qualified_domain_name:port_number/pds
        
        Where port is the application port set in config.py. By default its 5000

###  Step 9: (Optional) Custom configuration
Update configuration file at /opt/PDS/src/config/config.py for custom settings like changing default location of "distro data" or enabling/disabling logs


### _**Note:**_
* Alternatively we can also deploy PDS on Apache server by following steps from [Apache deployment](ApacheDeployment.md)

# Enabling and disabling debug logging

By default logging is disabled. To enable logs, following steps need to be followed:

### Step 1: Edit the file `/opt/PDS/src/config/config.py` as shown below:
```diff
@@ -12,7 +12,7 @@
-local_setup = False
+local_setup = True

```
### Step 2: Set `LOG_FILE_LOCATION` (Optional).

The following is the default location for data file and log file respectively:

	DATA_FILE_LOCATION = '/opt/PDS/src/distro_data'
	LOG_FILE_LOCATION = '/opt/PDS/log/pds.log'

### Step 3: Restart PDS application and the logs will be generated at the location configured in above step.

	sudo service pds restart
