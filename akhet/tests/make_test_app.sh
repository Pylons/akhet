#!/bin/bash -ex
# Make a test app 'Zzz' in the current directory and run it.

APPNAME=Zzz

if [ -e $APPNAME ] ;then
    echo -n 1>&2 "Error: test app '$APPNAME' exists, aborting."
    echo 1>&2 "  Suggested command line:"
    echo 1>&2 "rm -rf $APPNAME && bash $0"
    exit 1
fi

paster create -t akhet $APPNAME $*
cd $APPNAME
pip install -r requirements.txt
python setup.py egg_info
paster serve development.ini
