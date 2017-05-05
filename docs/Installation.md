# Steps for setting up PDS application on server

The instructions provided below specify the steps for SLES 11 SP4/12/12 SP1/12 SP2 and Ubuntu 16.04/16.10/17.04:

### Step 1: Install pre-requisite dependencies
Note: make sure you are logged in as user with sudo permissions

* For SLES (11 SP4, 12, 12 SP1, 12 SP2):

        sudo zypper install -y python python-setuptools gcc git libffi-devel python-devel openssl openssl-devel cronie python-xml pyxml tar wget aaa_base which w3m
        sudo easy_install pip

* For Ubuntu (16.04, 16.10, 17.04):

        sudo apt-get update
        sudo apt-get install -y python python-pip gcc git python-dev libssl-dev libffi-dev cron python-lxml apache2 libapache2-mod-wsgi

**Note:** if "/usr/local/bin" is not part of $PATH add it to the path:

        echo $PATH
        export PATH=/usr/local/bin:$PATH
        sudo sh -c "echo 'export PATH=/usr/local/bin:$PATH' > /etc/profile.d/alternate_install_path.sh"

### Step 2: Install Apache package and dependencies
        sudo zypper install -y apache2 apache2-devel apache2-worker apache2-worker apache2-mod_wsgi

### Step 2: Install Python dependencies libraries

        sudo pip install 'cryptography==1.4' Flask launchpadlib simplejson logging


###  Step 3: Checkout the source code, into /opt/ folder

        cd /opt/
        sudo git clone https://github.com/linux-on-ibm-z/PDS.git
        cd PDS

Note: In case PDS code is already checked out, but there is a new update to be fetched from repository, it should be updated as

        cd /opt/PDS
        sudo git pull origin master

###  Step 4: Set Environment variables

        sudo sh -c "echo 'export PYTHONPATH=/opt/PDS/src/classes:/opt/PDS/src/config:$PYTHONPATH' > /etc/profile.d/pds.sh"

### Step 5: Configure Apache to execute Flask code using WSGI
 Copy the apache configuration file from /opt/PDS/src/config/pds.conf into respective apache configuration folder as below

* SLES (12 SP1, 12 SP2):

        sudo cp -f /opt/PDS/src/config/pds.conf /etc/apache2/conf.d/pds.conf

* For Ubuntu (16.04, 16.10, 17.04):

        sudo cp -f /opt/PDS/src/config/pds.conf /etc/apache2/sites-enabled/pds.conf
        sudo mv /etc/apache2/sites-enabled/000-default.conf /etc/apache2/sites-enabled/z-000-default.conf

### Step 6: Create new user and group for apache
    sudo useradd apache
    sudo groupadd apache

### Step 7: (Only For SLES 12 SP1, 12 SP2) Enable authorization module in apache configuration
    sudo a2enmod mod_access_compat

### Step 8: Set appropriate folder and file permission on /opt/PDS/ folder for apache
    sudo chown -R apache:apache /opt/PDS/

### Step 9: Start/Restart Apache service
    sudo apachectl restart

###  Step 10: (Only For SLES 11 SP4, 12) Copy the init.d script to start/stop/restart PDS application
        sudo chmod 755 -R /opt/PDS/src/setup
        cd /opt/PDS/src/setup
        sudo ./create_initid_script.sh

###  Step 11: (Only For SLES 11 SP4, 12) Enable pds service

* For SLES (11 SP4, 12):

        sudo systemctl reload pds
        
###  Step 12: Start the Flask server as below

        sudo service pds start

###  Step 13: Verify that the server is up, by running the application in browser
        http://server_ip_or_fully_qualified_domain_name:port_number/pds
        
        Where port is the application port set in config.py. By default its 5000

###  Step 14: (Optional) Custom configuration
Update configuration file at /opt/PDS/src/config/config.py for custom settings like changing default location of "distro data" or enabling/disabling logs


### _**Note:**_
* Deploying application on Flask developer server has limitations, hence its not recommended to deploy the application on the same. 

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
