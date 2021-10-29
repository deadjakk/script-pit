#!/bin/bash
if [ $( id -u ) -ne 0 ]; then
echo must be root to install;
exit
fi

pip install -r requirements.txt --user
install *.py /usr/local/bin/

cd ./ldapdomaincustom
pip install -r requirements.txt --user
install *.py /usr/local/bin/
