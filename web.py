# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 22:34:56 2024

@author: Patrick
"""

from nicegui import ui
import chromadb
from functools import wraps, partial
import asyncio

COLLECTION_NAME = "MrCarlsonsLab"
PATH = "db/"+COLLECTION_NAME

#collection = None
results = []

#def connect():
client = chromadb.PersistentClient(path=PATH)
collection = client.get_collection(name=COLLECTION_NAME)

def wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run


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
    results = collection.query(query_texts=[qstr], n_results=n) 
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

@wrap
def populate():
    results = []
    query = search.value
    if query:    
        results = get_results(qstr=query, n=5)
    if results:
        resDiv.clear()
        with resDiv:
            ui.label('Results').style('font-size: 125%').classes('bg-slate-300 w-full')
            for entry in results:
                formatted_timestamp = format_timestamp( entry['metadatas']['timestamp'] )
                vid = entry['metadatas']['video']
                youtube_url = f"https://www.youtube.com/watch?v={vid}&t={formatted_timestamp}"
                title = entry['metadatas']['title']
                with ui.row().classes('border-2 border-slate-600 p-2 items-center mt-2 hover:bg-amber-100'):
                    ui.image(f"https://img.youtube.com/vi/{vid}/hqdefault.jpg").style('width: 240px;')
                    with ui.column().style().classes().style('width: 320px;'):
                        ui.link(f"{title} ({formatted_timestamp})", youtube_url).classes('text-pretty').style('font-size: 115%;')
                        ui.space()
                        ui.label("..."+entry['documents']+"...").style('font-size: 115%; font-style: italic')

with ui.row().classes('w-full gap-2'):
    with ui.column().classes().style():
        ui.label(f'Search {COLLECTION_NAME}').style('font-size: 125%').classes('w-full text-center bg-slate-300')
        with ui.row():
            search = ui.input(placeholder='combating noise').props('rounded outlined clearable dense').style('font-size: 125%; width: 500px;')
            ui.button(icon='search', on_click=populate)
        ui.label('  ')
        resDiv = ui.element('div').classes()


ui.run()

