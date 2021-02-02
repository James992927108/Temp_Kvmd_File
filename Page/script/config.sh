#!/bin/sh

echo "Setup the environment variable.."
export BOARD='generic'
export ARCH='aarch64'
# export ARCH='arm'
export PLATFORM='v2-hdmiusb'
export LOCALE='en_US'
export TIMEZONE='Asia/Taipei'
export REPO_URL='http://mirror.archlinuxarm.org'

# export BUILDER_URL='https://github.com/mdevaev/pi-builder'
# export PIKVM_REPO_URL = https://pikvm.org/repos
# export PIKVM_REPO_KEY = 912C773ABBD1B584

export BUILDER_URL = 'https://github.com/Yura80/pi-builder'
export PIKVM_REPO_URL='https://raw.githubusercontent.com/Yura80/pikvm-repo/main'
export PIKVM_REPO_KEY='39CCCE14BFBB5D69'

export _BUILDER_DIR='./pi-builder'
# export NEW_HTTPS_CERT=

# echo "Go to init.sh.."
# source ./init.sh

echo "Go to os.sh.."
. ./os.sh

echo "Go to pikvm-repo.sh.."
. ./pikvm-repo.sh

echo "Go to pikvm.sh.."
. ./pikvm.sh