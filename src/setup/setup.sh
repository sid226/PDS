# This script will be in working condition for SLES 
DEPLOY_PATH="/var/www/html/PDS"

echo "export PYTHONPATH=`pwd`/../" > /tmp/pds.sh

mv /tmp/pds.sh /etc/profile.d/.

CONFIG_PATH="/etc/httpd/conf.d/"
CONFIG_FILE="pds.conf"

# Clean if old codebase is found.
rm -rf $DEPLOY_PATH/

rm -f $CONFIG_PATH

# Now start copying fresh codebase

echo "Copying autoport to webroot"

mkdir -p $DEPLOY_PATH

cp -rf ../* $DEPLOY_PATH

echo "Completed copying PDS tool to webroot"

cp -f ../config/$CONFIG_FILE $CONFIG_PATH/pds.conf

echo "WSGISocketPrefix /var/run/wsgi" >> /etc/apache2/httpd.conf

cd $DEPLOY_PATH

find . -type f -exec chmod 0644 {} \;

find . -type d -exec chmod 0755 {} \;

# SELinux related settings
chcon -t httpd_sys_content_t $DEPLOY_PATH -R
chcon -t httpd_sys_rw_content_t $DEPLOY_PATH/data -R
setsebool -P httpd_can_network_connect 1
#chown -R apache:apache $DEPLOY_PATH
service httpd restart
