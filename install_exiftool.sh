#!/bin/bash

#download and install the exiftool package
#https://exiftool.org/install.html#Unix

wget -O $HOME/ExifTool.tar.gz https://exiftool.org/Image-ExifTool-12.22.tar.gz
tar -C $HOME -zxvf $HOME/ExifTool.tar.gz
cd $HOME/Image-ExifTool-12.22 
perl Makefile.PL
make test
sudo make install








