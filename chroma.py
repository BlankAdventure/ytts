# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 16:12:02 2024

@author: BlankAdventure
"""

import videos
import chromadb

client = chromadb.Client()
client.delete_collection("my-collection")
collection = client.create_collection("my-collection")


#vid_ids = videos.get_video_ids()

# for testing just want a few entries

videos.add_to_db(['xY49YWDcKWE'], collection)

# docs1=["This is a document about cat"]
# meta1=[{"category": "animal"}]
# ids1=["id1"]

# collection.add(documents=docs1, metadatas=meta1, ids=ids1)

# docs2=["a thing about dogs"]
# meta2=[{"category": "animal"}]
# ids2=["id2"]
