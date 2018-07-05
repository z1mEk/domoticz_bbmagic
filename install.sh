#!/bin/sh
## prepare library bbmagic_lib_x.x.a to dynamic library bbmagic_lib_x.x.so
## install library to /usr/lib

libv="1.2"

wget http://bbmagic.net/download/bin/bbmagic_lib_$libv.tar.gz
tar -zxvf bbmagic_lib_$libv.tar.gz
cd bbmagic_lib_$libv
ar -xv bbmagic_lib_$libv.a bbmagic_lib_$libv.o
wget http://bbmagic.net/download/bin/libbluetooth.a
gcc -shared -o bbmagic_lib_$libv.so bbmagic_lib_$libv.o libbluetooth.a
cp bbmagic_lib_$libv.so /usr/lib/bbmagic_lib_$libv.so
cd ..
rm -r ./bbmagic_lib_$libv
rm bbmagic_lib_$libv.tar.gz
wget https://raw.githubusercontent.com/z1mEk/bbmagic_python_class/master/bbm_class.py
echo "Done."
