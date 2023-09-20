#!/bin/bash

# has to be run from the quantum-play repo, subdir install_scripts/topaz/

py_ver="3.10.10"
pip_ver="23.1.2"
st_ver="68.0.0"

module load maali/1.8.4
mkdir -p $MYGROUP/software/centos7.6/modulefiles
module use $MYGROUP/software/centos7.6/modulefiles

sed -i "s;\"setuptools/.*\";\"setuptools/$st_ver\";g" pip.cyg

# from rpm -ql openssl11-libs-1.1.1k-3.el7.x86_64 |grep lib64
lib_list="/usr/lib64/.libcrypto.so.1.1.1k.hmac
/usr/lib64/.libcrypto.so.1.1.hmac
/usr/lib64/.libssl.so.1.1.1k.hmac
/usr/lib64/.libssl.so.1.1.hmac
/usr/lib64/libcrypto.so.1.1
/usr/lib64/libcrypto.so.1.1.1k
/usr/lib64/libssl.so.1.1
/usr/lib64/libssl.so.1.1.1k"
lib_list_eng="/usr/lib64/engines-1.1/afalg.so
/usr/lib64/engines-1.1/capi.so
/usr/lib64/engines-1.1/padlock.so
"
mkdir -p lib/engines-1.1
cd lib
for l in $lib_list ; do
  ln -s $l .
done
for l in $lib_list_eng ; do
  cd engines-1.1
  ln -s $l .
  cd ..
done
ln -s libssl.so.1.1 libssl.so
ln -s libcrypto.so.1.1 libcrypto.so
cd ..
mkdir include
cd include
ln -s /usr/include/openssl .
cd ..
export LIBRARY_PATH="$(pwd)/lib:$LIBRARY_PATH"
export LD_LIBRARY_PATH="$(pwd)/lib:$LD_LIBRARY_PATH"
export CPATH="$(pwd)/include:$CPATH"

cp -p python.cyg BKP.python.cyg
sed -i "s;--with-openssl.*;--with-openssl=$(pwd) --with-openssl-rpath=$(pwd)/lib;g"  python.cyg
maali -t Python -v $py_ver
mv BKP.python.cyg python.cyg

export MAALI_DEFAULT_PYTHON=python/$py_ver
maali -t setuptools -v $st_ver
maali -t pip -v $pip_ver
