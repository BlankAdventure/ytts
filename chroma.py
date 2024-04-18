# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 16:12:02 2024

@author: BlankAdventure
"""

import videos
import chromadb

COLLECTION_NAME = "MrCarlsonsLab"
PATH = "db/"+COLLECTION_NAME

client = chromadb.PersistentClient(path=PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

vid_ids = videos.get_video_ids(channel=COLLECTION_NAME)

# for testing just want a few entries

videos.add_to_db(vid_ids, collection)


#results = collection.query(query_texts=['shielding'])

# docs1=["This is a document about cat"]
# meta1=[{"category": "animal"}]
# ids1=["id1"]

# collection.add(documents=docs1, metadatas=meta1, ids=ids1)

# docs2=["a thing about dogs"]
# meta2=[{"category": "animal"}]
# ids2=["id2"]
