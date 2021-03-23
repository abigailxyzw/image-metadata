import pandas as pd
import pdb
import sys
import json
import os

def read_one_drop(drop_dict, drop_number):
    drop_number = drop_number
    try:
        name = drop_dict["name"]
    except KeyError:
        name = None
    try:
        trip_code = drop_dict['trip']
    except KeyError:
        trip_code = None
    try:
        user_id = drop_dict['userId']
    except KeyError:
        user_id = None
    try:
        post_id = drop_dict['id']
    except KeyError:
        post_id = None
    try:
        timestamp = drop_dict['timestamp']
    except KeyError:
        timestamp = None
    try:
        source = drop_dict['source']
    except KeyError:
        source = None
    try:
        link = drop_dict['link']
    except KeyError:
        link = None
    return name, trip_code, drop_number, user_id, post_id, timestamp, source, link

def parse_json():

    print("First parsing posts.json")
    script_folderpath=os.path.dirname(os.path.abspath(__file__))
    json_filepath=os.path.join(script_folderpath, 'data/all_drops/posts.json')
    tsv_filepath=os.path.join(script_folderpath, 'data/all_drops/all_drops.tsv') 

    with open(json_filepath, 'r') as fh:
        drop_list = json.load(fh)

    num_drops = len(drop_list)
    names = []
    trip_codes = []
    drop_numbers = []
    post_ids = [] 
    timestamps = []
    user_ids = []
    sources = []
    links = []
    
    for i, drop_dict in enumerate(drop_list):
        drop_number = num_drops - i 
        try:
            name, trip_code, drop_number, user_id, post_id, timestamp, source, link = read_one_drop(drop_dict, drop_number)
            names.append(name)
            trip_codes.append(trip_code)
            drop_numbers.append(drop_number)
            user_ids.append(user_id)
            post_ids.append(post_id)
            timestamps.append(timestamp)
            sources.append(source)
            links.append(link)
        except:
            sys.stderr.write("Cannot process drop %s" % page_num)
    data_dict = {'name': names, 'trip_code': trip_codes, 'drop_number': drop_numbers, 'post_id': post_ids, 'timestamp': timestamps, 'user_id': user_ids, 'source': sources, 'link': links}
    df=pd.DataFrame(data_dict)
    df.sort_values(by=['drop_number'], axis=0, inplace=True)
    df.index=range(1, num_drops+1)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
    df.to_csv(tsv_filepath, index=False)


