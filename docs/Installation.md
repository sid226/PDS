# Steps for setting up PDS application on server

The instructions provided below specify the steps for SLES 11 SP4/12/12 SP1/12 SP2 and Ubuntu 16.04/16.10/17.04:

_**NOTE:**_
* make sure you are logged in as user with sudo permissions

### Step 1: Install pre-requisite

* For SLES (11 SP4, 12, 12 SP1, 12 SP2):

        sudo zypper install -y python python-setuptools gcc git libffi-devel python-devel openssl openssl-devel cronie python-xml pyxml tar wget aaa_base which w3m
        sudo easy_install pip
        sudo pip install 'cryptography==1.4' Flask launchpadlib simplejson logging

* For Ubuntu (16.04, 16.10, 17.04):

        sudo apt-get update
        sudo apt-get install -y python python-pip gcc git python-dev libssl-dev libffi-dev cron python-lxml apache2 libapache2-mod-wsgi
        sudo pip install 'cryptography==1.4' Flask launchpadlib simplejson logging

* Apache:
    * For SLES (12 SP1, 12 SP2):

            sudo zypper install -y apache2 apache2-devel apache2-worker apache2-mod_wsgi

**Note:** 
* if "/usr/local/bin" is not part of $PATH add it to the path:

        echo $PATH
        export PATH=/usr/local/bin:$PATH
        sudo sh -c "echo 'export PATH=/usr/local/bin:$PATH' > /etc/profile.d/alternate_install_path.sh"

* On SLES 11 SP4 and SLES 12 module apache2-mod_wsgi is not supported completely.


###  Step 2: Checkout the source code, into /opt/ folder

        cd /opt/
        sudo git clone https://github.com/linux-on-ibm-z/PDS.git
        cd PDS

Note: In case PDS code is already checked out, but there is a new update to be fetched from repository, it should be updated as

        cd /opt/PDS
        sudo git pull origin master

###  Step 3: Set Environment variables

        sudo sh -c "echo 'export PYTHONPATH=/opt/PDS/src/classes:/opt/PDS/src/config:$PYTHONPATH' > /etc/profile.d/pds.sh"

### Step 4: Install and configure PDS

* SLES (11 SP4, 12):

    * Copy the init.d script to start/stop/restart PDS application

        ```
        sudo chmod 755 -R /opt/PDS/src/setup
        cd /opt/PDS/src/setup
        sudo ./create_initid_script.sh
        ```

    * Enable pds service

        ```sudo systemctl reload pds```

    * Start the Flask server as below

        ```sudo service pds start```

* SLES (12 SP1, 12 SP2) and Ubuntu (16.04, 16.10, 17.04):

    * Copy the apache configuration file from `/opt/PDS/src/config/pds.conf` into respective apache configuration folder as below

        * SLES (12 SP1, 12 SP2):

                sudo cp -f /opt/PDS/src/config/pds.conf /etc/apache2/conf.d/pds.conf

        * For Ubuntu (16.04, 16.10, 17.04):

                sudo cp -f /opt/PDS/src/config/pds.conf /etc/apache2/sites-enabled/pds.conf
                sudo mv /etc/apache2/sites-enabled/000-default.conf /etc/apache2/sites-enabled/z-000-default.conf

    * Create new user and group for apache

        ```
        sudo useradd apache
        sudo groupadd apache
        ```

    * Enable authorization module in apache configuration

        ```sudo a2enmod mod_access_compat```

    * Set appropriate folder and file permission on /opt/PDS/ folder for apache

        ```sudo chown -R apache:apache /opt/PDS/```

    * Start/Restart Apache service

        ```sudo apachectl restart```

###  Step 5: Verify that the PDS server is up and running

```http://server_ip_or_fully_qualified_domain_name:port_number/pds```

_**NOTE:**_ 

* For SLES (11 SP4, 12) the `port_number` will be 5000 by default
* For SLES (12 SP1, 12 SP2) and Ubuntu (16.04, 16.10, 17.04) `port_number` will be 80 by default

###  Step 10: (Optional) Custom configuration
Update configuration file at `/opt/PDS/src/config/config.py` for custom settings like changing default location of "distro data" or enabling/disabling logs

