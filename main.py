import os
import json
import pdb
import pandas as pd
import re
import numpy as np
import argparse
from numpy import nan
from setup import download_images, move_pngs_over, get_q_pngs

def parse_args():
    parser = argparse.ArgumentParser(description='Helper routines to analyze a subset of image metadata from Q posts')
    parser.add_argument('--subset_images', action='store_true', help='Extract only the images posted by Q, excluding those from anons.')
    parser.add_argument("--create_data_set", action="store_true", help='Create dataset of metadata from Q images labeled "Screenshot')
    parser.add_argument("--visualize", action="store_true", help='Create visualizations of time difference information')
    parser.add_argument("--download_images", action="store_true", help='Create visualizations of time difference information')

    args=parser.parse_args()
    return args

class MetaDataManager():
    def __init__(self, blacklist=False):
        self.blacklist=blacklist

        #filepaths
        self.posts_fp=os.path.join(os.getenv("HOME"), 'image-metadata/data/posts.json')
        self.imagemd_fp=os.path.join(os.getenv("HOME"), 'image-metadata/data/metadata.csv')
        self.counts_fp=os.path.join(os.getenv("HOME"), 'image-metadata/analysis/txt/counts.csv')
        self.blacklist_fp=os.path.join(os.getenv("HOME"), 'image-metadata/analysis/txt/blacklist.csv')
        self.metadata_decorated_fp=os.path.join(os.getenv("HOME"), 'image-metadata/analysis/txt/metadata_decorated.csv')
        self.screenshots_fp=os.path.join(os.getenv("HOME"), 'image-metadata/analysis/txt/screenshots.csv')
        
        self.imagemd_df=None
        self.posts_json=None
        self.blacklist_df=None
        
        self.metadata_decorated_df=None
        self.screenshots_df=None
        self.media_info_df=None
        self.counts_dict=None

        #sets self.imagemd_df
        self.get_image_metadata()
        #sets self.posts_json
        self.get_posts()
        #reads self.blacklist_df
        self.get_blacklist()
        self.num_drops=len(self.posts_json)
            
    def get_image_metadata(self):
        if not self.imagemd_df:
            self.imagemd_df=pd.read_csv(self.imagemd_fp, index_col=False)

    def get_posts(self):
        if not self.posts_json:
            with open(self.posts_fp, 'r') as fh:
                self.posts_json=json.load(fh)

    def get_blacklist(self):
        if not self.blacklist_df and self.blacklist:
            self.blacklist_df=pd.read_csv(self.blacklist_fp, names=['drop_number'], dtype={'drop_number':str}, index_col=False)

    def get_media_duplicates(self):
        if not self.counts_dict:
            png_counts={}
            for i, drop in enumerate(self.posts_json):
                drop_number=str(self.num_drops - i)
                try:
                    media=drop['media']
                except KeyError:
                    continue
                if media is not None and len(media) > 0:
                    #pdb.set_trace()
                    for m in media:
                        q_png_fp_long=m['url']
                        q_png_fp=os.path.basename(q_png_fp_long)
                        if q_png_fp not in png_counts:
                            png_counts[q_png_fp]=[]
                        png_counts[q_png_fp].append(drop_number)
            counts_dict={}
            for k, v in png_counts.items():
                counts_dict[k]=[len(v), v]
            self.counts_dict=counts_dict
            with open(self.counts_fp, 'w') as fh:
                json.dump(self.counts_dict, fh, indent=4)

    def get_media_with_extra_fields(self):
        if not self.media_info_df:
            pngs=[]
            drop_ids=[]
            timestamps=[]
            drop_nums=[]
            trips=[]
            sources=[]
            for i, drop in enumerate(self.posts_json):
                drop_number=str(self.num_drops - i)
                try:
                    media=drop['media']
                except KeyError:
                    continue
                try:
                    drop_id=drop['id']
                except:
                    continue
                try:
                    timestamp=drop['timestamp']
                    if timestamp is None:
                        timestamp='NA'
                except KeyError:
                    timestamp='NA'
                try:
                    source=drop['source']
                    if source is None:
                        source='NA'
                except KeyError:
                    source='NA'
                try:
                    trip=drop['trip']
                    if trip is None:
                        trip='NA'
                except KeyError:
                    trip='NA'
                if media is not None and len(media) > 0:
                    for m in media:
                        q_png_fp_long=m['url']
                        q_png_fp=os.path.basename(q_png_fp_long)
                        pngs.append(q_png_fp)
                        drop_ids.append(drop_id)
                        timestamps.append(timestamp)
                        drop_nums.append(drop_number)
                        trips.append(trip)
                        sources.append(source)
        self.media_info_df=pd.DataFrame({'SourceFileShort':pngs, 'drop_id': drop_ids, 'timestamp': timestamps, 'drop_number': drop_nums, 'trip': trips, 'source': sources})
        
    def get_metadata_decorated(self):
        if not self.metadata_decorated_df:
            #dependencies
            self.get_media_with_extra_fields()
            self.get_media_duplicates()
            counts_short={}
            for k,v in self.counts_dict.items():
                counts_short[k]=v[0]
            counts_df=pd.DataFrame({'SourceFileShort': counts_short.keys(), 'times_Q_used': counts_short.values()})
            self.imagemd_df['SourceFileShort']=self.imagemd_df['SourceFile'].apply(lambda x: os.path.basename(x))
            merged=pd.merge(self.media_info_df, self.imagemd_df, on=['SourceFileShort'], how='inner')
            self.metadata_decorated_df=pd.merge(merged, counts_df, on=['SourceFileShort'], how='inner')
            if self.blacklist:
                blacklisted=blacklist_df.drop_number.values.tolist()
                self.metadata_decorated_df=self.metadata_decorated_df[~self.metadata_decorated_df.drop_number.isin(blacklisted)]    
            self.metadata_decorated_df['timestamp'] = pd.to_datetime(self.metadata_decorated_df['timestamp'], unit='s', utc=True) 
            self.metadata_decorated_df.rename(columns={'timestamp': 'timestamp_drop_UTC'}, inplace=True)
            self.metadata_decorated_df.to_csv(self.metadata_decorated_fp, index=False)


    def get_screenshot_info(self):
        if not self.screenshots_df:
            self.get_metadata_decorated()
            stack_two_df=self.metadata_decorated_df[self.metadata_decorated_df.UserComment == 'Screenshot']
            stack_two_df['DateCreated']=pd.to_datetime(stack_two_df['DateCreated'], format='%Y:%m:%d %H:%M:%S', utc=True)
            stack_two_df['timediff']=stack_two_df['DateCreated']-stack_two_df['timestamp_drop_UTC']
            stack_two_df['timediff']=stack_two_df.timediff.dt.total_seconds()/3600.
            stack_two_df['DateCreated']=stack_two_df['DateCreated'].dt.tz_localize(None)
            cols=stack_two_df.columns.tolist()
            re_org=['drop_number', 'timestamp_drop_UTC', 'DateCreated', 'timediff', 'source', 'trip']
            for re in re_org:
                cols.remove(re)
                cols=re_org + cols
            stack_two_df=stack_two_df[cols]
            self.screenshots_df=stack_two_df
            self.screenshots_df.to_csv(self.screenshots_fp,  index=False)

if __name__=="__main__":

    args=parse_args() 
   
    if args.download_images:
        download_images()

    if args.subset_images:
        posts_fp=os.path.join(os.getenv("HOME"), 'image-metadata/data/posts.json')
        with open(posts_fp, 'r') as fh:
            post_dict=json.load(fh)
        full_folder_from=os.path.join(os.getenv("HOME"), 'image-metadata/media/downloads')
        full_folder_to=os.path.join(os.getenv("HOME"), 'image-metadata/media/just_q')
        q_pngs=get_q_pngs(post_dict)
        move_pngs_over(q_pngs, full_folder_from, full_folder_to)

    if args.create_data_set:
        my_mdm=MetaDataManager()
        my_mdm.get_screenshot_info()

    if args.visualize:
        pass


