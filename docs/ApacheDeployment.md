# Deploy PDS on Apache server

The instructions provided below specify the steps for SLES 12 SP1/12 SP2 and Ubuntu 16.04/16.10/17.04:

### Step 1: Install Apache web server and mod_wsgi for python support
Note: make sure you are logged in as user with sudo permissions

* SLES (12 SP1, 12 SP2):

        sudo zypper install -y apache2 apache2-devel apache2-worker apache2-mod_wsgi which w3m

* For Ubuntu (16.04, 16.10, 17.04):

        sudo apt-get update
        sudo apt-get install -y apache2 libapache2-mod-wsgi

### Step 2: Configure Apache to execute Flask code using WSGI
 Copy the apache configuration file from /opt/PDS/src/config/pds.conf into respective apache configuration folder as below

* SLES (12 SP1, 12 SP2):

        sudo cp -f /opt/PDS/src/config/pds.conf /etc/apache2/conf.d/pds.conf

* For Ubuntu (16.04, 16.10, 17.04):

        sudo cp -f /opt/PDS/src/config/pds.conf /etc/apache2/sites-enabled/pds.conf
        sudo mv /etc/apache2/sites-enabled/000-default.conf /etc/apache2/sites-enabled/z-000-default.conf

### Step 3: Create new user and group for apache
    sudo useradd apache
    sudo groupadd apache

### Step 4: (Only For SLES 12 SP1, 12 SP2) Enable authorization module in apache configuration
    sudo a2enmod mod_access_compat

### Step 5: Set appropriate folder and file permission on /opt/PDS/ folder for apache
    sudo chown -R apache:apache /opt/PDS/

### Step 6: Start/Restart Apache service
    sudo apachectl restart


###  Step 7: Verify that the server is up, by running the application in browser
        http://server_ip_or_fully_qualified_domain_name:port_number/pds

        Where port is the application port set in pds.conf at Step 2. By default its 80
