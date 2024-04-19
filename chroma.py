# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 16:12:02 2024

@author: BlankAdventure
"""

# *****************************************************************************
# Example script for building a chromadb embeddings vector database from
# from a specified YouTube channel
# *****************************************************************************

import os
import videos
import chromadb

# Adds transcript entries to a chromadb collection
def add_to_db(vid_ids: list[str], collection) -> list[str]:
    failed = []
    for entry in videos.entry_generator(vid_ids):
        if entry:
            collection.add(documents=[entry['text']], metadatas=[entry['metadata']], ids=[entry['uid']])
        else:
            failed.append(entry)
    return failed

# Top-level function for building a chromadb embeddings vector database from
# a specified YouTube channel. The channel name should be the part after the 
# @ symbol
def build_db(channel_name: str, path: str = '.'):
    full_path = os.path.normpath(os.path.join(os.path.abspath(path),channel_name))
    print(f'SAVING TO: {full_path}') #show full path to stored db
    client = chromadb.PersistentClient(path=full_path)
    collection = client.get_or_create_collection(name=channel_name)    
    print('Getting video list...')
    vid_ids = videos.get_video_ids(channel=channel_name)
    add_to_db(vid_ids, collection) #modify-in-place operation
    return collection


