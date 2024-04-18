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

# Name of channel to process 
COLLECTION_NAME = "MrCarlsonsLab"
PATH = "db/"+COLLECTION_NAME
full_path = os.path.normpath(os.path.join(os.getcwd(),PATH))


client = chromadb.PersistentClient(path=PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

vid_ids = videos.get_video_ids(channel=COLLECTION_NAME)
print(f'SAVED TO: {full_path}') #show full path to stored db

videos.add_to_db(vid_ids, collection)

# Example query
results = collection.query(query_texts=['how to solve noise issues?'])