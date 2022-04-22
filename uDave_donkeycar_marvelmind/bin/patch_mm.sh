#!/bin/bash
shopt -s globstar

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ENV_DIR="$(dirname "$SCRIPT_DIR")"
DC_DIR="donkeycar"
MYCAR_DIR="mycar"


function do_patch(){
  echo "Copy marvelmind.py into $DC_DIR/donkeycar/parts/"
  cp -v $ENV_DIR/$DC_DIR/donkeycar/parts/marvelmind.py $HOME/$DC_DIR/donkeycar/parts

  echo "Patch $HOME/$MYCAR_DIR/manage.py and $HOME/$MYCAR_DIR/myconfig.py"
  patch -bu $HOME/$MYCAR_DIR/manage.py $ENV_DIR/$MYCAR_DIR/manage.py.patch --verbose
  patch -bu $HOME/$MYCAR_DIR/myconfig.py $ENV_DIR/$MYCAR_DIR/myconfig.py.patch --verbose
}

function do_unpatch(){
  echo "Remove marvelmind.py from $DC_DIR/donkeycar/parts"
  rm -vf $HOME/$DC_DIR/donkeycar/parts/marvelmind.py

  echo "Try unptach $MYCAR_DIR/manage.py and $MYCAR_DIR/myconfig.py"
  patch -Ru $HOME/$MYCAR_DIR/manage.py $ENV_DIR/$MYCAR_DIR/manage.py.patch --verbose
  patch -Ru $HOME/$MYCAR_DIR/myconfig.py $ENV_DIR/$MYCAR_DIR/myconfig.py.patch --verbose
}

case $1 in
  patch)
    do_patch
    ;;
  unpatch)
    do_unpatch
    ;;
  "")
    do_patch
    ;;
  *)
    echo "wrong argument! [patch|unpatch]"
    ;;
esac

shopt -u globstar
unset SCRIPT_DIR DC_DIR MYCAR_DIR do_patch do_unpatch
