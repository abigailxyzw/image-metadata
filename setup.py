import json
import requests
import pdb
import os
#import time

def download_images():
    cloud_folder='https://qalerts.net/media/'
    output_folder=os.path.join(os.getenv("HOME"), 'image-metadata/media/downloads')
    res=requests.get(cloud_folder)
    files=res.json()
    for f in files:
       print("Downloading %s" % f)
       filename=os.path.basename(f)
       output_fp=os.path.join(output_folder, filename)
       r = requests.get(f, allow_redirects=True)
       open(output_fp, 'wb').write(r.content)

def get_q_pngs(post_dict):
    q_pngs=[]
    for drop in post_dict:
        try:
            media=drop['media']
        except KeyError:
            continue
        if media is not None and len(media) > 0:
            for m in media:
                q_png_fp_long=m['url']
                q_png_fp=os.path.basename(q_png_fp_long)
                if q_png_fp not in q_pngs:
                    q_pngs.append(q_png_fp)
    q_pngs.reverse()
    return q_pngs

#move pngs over
def move_pngs_over(q_pngs, full_folder_from, full_folder_to):
    for q_png in q_pngs:
        full_fp_from='%s/%s' % (full_folder_from, q_png)
        full_fp_to='%s/%s' % (full_folder_to, q_png)
        os.system('mv %s %s' % (full_fp_from, full_fp_to))  

if __name__=="__main__":
    download_images()
