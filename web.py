# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 22:34:56 2024

@author: Patrick
"""

from nicegui import ui
import chromadb

COLLECTION_NAME = "MrCarlsonsLab"
PATH = "db/"+COLLECTION_NAME

#collection = None
results = []

#def connect():
client = chromadb.PersistentClient(path=PATH)
collection = client.get_collection(name=COLLECTION_NAME)


def format_timestamp(timestamp):
    hours = int(timestamp / 3600)
    minutes = int((timestamp % 3600) / 60)
    seconds = int(timestamp % 60)
    return f"{hours}h{minutes}m{seconds}s"

def display_youtube_videos(video_ids, timestamps=None):
    if timestamps is None:
        timestamps = [0] * len(video_ids)

    for video_id, timestamp in zip(video_ids, timestamps):
        formatted_timestamp = format_timestamp(timestamp)
        youtube_url = f"https://www.youtube.com/watch?v={video_id}&t={formatted_timestamp}"
        ui.image(f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg").style('width: 320px;')
        ui.link(youtube_url, f"Watch on YouTube (Jump to {formatted_timestamp})")



def get_results(qstr: str, n=5):
    transformed_list = []
    results = collection.query(query_texts=['how to solve noise issues?'], n_results=n) 
    remove = ('data', 'uris', 'embeddings')
    for k in remove:
        results.pop(k, None)
    num_entries = len(results['ids'][0])    
    for i in range(num_entries):
        entry = {}
        for key, values in results.items():
            entry[key] = values[0][i]
        transformed_list.append(entry)  
    return transformed_list

def populate():
    results = get_results(qstr=None, n=5)
    print(results)
    with resDiv:
        vids = [results[x]['metadatas']['video'] for x in range(3)]
        ts = [results[x]['metadatas']['timestamp'] for x in range(3)]
        display_youtube_videos(vids, ts)
        #for entry in results:
        #    pass

with ui.row().classes('border w-full gap-2 bg-yellow-100'):
    with ui.column().classes('border bg-teal-50'):
        ui.label(f'Search {COLLECTION_NAME}').style('font-size: 125%')
        ui.input(placeholder='begin search').props('rounded outlined clearable dense').style('font-size: 125%; width: 500px;')
        ui.button('Search', on_click=populate)
    with ui.column().classes('border bg-green-50'):
        ui.label('Results')
        resDiv = ui.element('div').classes('border bg-red-50')
        populate()

#if collection is None:
#    connect()

ui.run()

