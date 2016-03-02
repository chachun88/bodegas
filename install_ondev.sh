#!/bin/sh

LOCALREPO_VC_DIR=/var/www/bgiani.ondev/.git

if [ ! -d $LOCALREPO_VC_DIR ]
then
    echo "cloning..."
    git clone http://ondev:loadingplay007@gogs.ondev.today/loadingplay/bodegas.git /var/www/bgiani.ondev/
fi

echo "cd to /var/www/sites.ondev"
cd /var/www/sites.ondev
unset GIT_DIR

echo "checkout"
git checkout master -f

echo "pull"
git pull

echo "init submodule"
git config submodule.dafiti.url http://ondev:loadingplay007@gogs.ondev.today/loadingplay/dafiti.git
git submodule update --init --recursive

echo "npm and bower"
npm install
bower install

echo "change permissions"
chmod +x install_ondev.sh
