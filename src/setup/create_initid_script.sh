PDS_PATH=/opt/PDS/src/setup

if [[ (-f /etc/SUSE-brand) || (-f /etc/SuSE-release) ]];then
    cp $PDS_PATH/pds /etc/init.d/.
    sed -i '6i. /etc/rc.status' /etc/init.d/pds
elif [[ -f /etc/os-release ]];then
    cp $PDS_PATH/pds /etc/init.d/.
    sed -i '6i. /lib/lsb/init-functions' /etc/init.d/pds
else
    echo "Currently only suporting Ubuntu/SLES"
fi