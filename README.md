README

**The author of this codebase approaches the Qanon phenomenon from a skeptical perspective.**

##Summary 

This python 3 codebase allows a user to create a dataset of metadata for the images posted by Q. It also produces a dataset of 29 images marked "Screenshot," 27 of which have time information. It is likely this metadata was added by Q's own device rather than inherited from another source. In any case, we have not been able to find the source for the metadata online using reverse image source and metadata extraction tools.

The author was able to run the code in python 3.8.5.

##Detailed Instructions

On ubuntu linux, the shell script *install_exiftool.sh* should download and install exiftool.  On other environments you should follow the installation process on the exiftool website (*https://exiftool.org/*).

The shell script *scrape_metadata.sh* assumes this repository is located in the user's home directory.  The script should set up folders, set up a virtual environment in the directory, download images and metadata, and create two datasets.  The initial run of the exiftool command should appear at *image-metadata/data/metadata.csv*. The final output of this script is a dataset of image metadata decorated with some information about the drops, which is useful for analysis.  This dataset will be located at *image-metadata/analysis/txt/metadata_decorated.csv*.

Those who wish to download the images and initial posts.json separately can do so from *https://qalerts.net/media/*and *https://qalerts.app/data/json/posts.json* for now.  (Take note: we are unaffiliated with qalerts, which is a Qanon-promoting website.)

To create the screenshots dataset, activate the virtual environment and run `python3 main.py --subset_images`. The dataset will be output to *image-metadata/analysis/txt/screenshots.csv.*

Finally, the ipython notebook *image-metadata-analysis.ipynb* reads in the screenshot data and performs analysis on its timestamps.

##Further Information

You can reach the code authors at abigail.wxyz@gmail.com and robertamourgoogs@gmail.com.