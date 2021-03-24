#!/bin/bash

#setup directories
mkdir $HOME/image-metadata/data
mkdir -p $HOME/image-metadata/analysis/txt
mkdir -p $HOME/image-metadata/analysis/viz
mkdir -p $HOME/image-metadata/media/downloads
mkdir -p $HOME/image-metadata/media/just_q

#activate virtual environment
echo "installing virtual environment"
mkdir $HOME/image-metadata/venv
python3 -m venv $HOME/image-metadata/venv
source $HOME/image-metadata/venv/bin/activate && pip3 install -r $HOME/image-metadata/requirements.txt

#download images to folder 
echo "downloading images"
python3 main.py --download_images

#download json to folder
#check behavior
wget https://qalerts.app/data/json/posts.json -P $HOME/image-metadata/data/ 

#sort images into Q/not Q
python3 $HOME/image-metadata/main.py --subset_images

#run exif tool
exiftool -csv $HOME/image-metadata/media/just_q/ > $HOME/image-metadata/data/metadata.csv






