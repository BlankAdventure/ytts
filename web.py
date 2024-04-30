# -*- coding: utf-8 -*-
"""

Created on Wed Apr 17 22:34:56 2024

@author: Patrick
"""

from nicegui import ui, run
import chromadb


COLLECTION_NAME = "MrCarlsonsLab"
PATH = "C:/LocalRepo/ytts/db/"+COLLECTION_NAME

results = []

client = chromadb.PersistentClient(path=PATH)
collection = client.get_collection(name=COLLECTION_NAME)

def format_timestamp(timestamp: float) -> str:
    hours = int(timestamp / 3600)
    minutes = int((timestamp % 3600) / 60)
    seconds = int(timestamp % 60)
    return f"{hours}h{minutes}m{seconds}s"

# Issue a querty to the database and return (cleaned up) results
def get_results(qstr: str, n=5) -> list[dict]:
    transformed_list = []
    results = collection.query(query_texts=[qstr], n_results=n) 
    remove = ('data', 'uris', 'embeddings') #Don't need these
    for k in remove:
        results.pop(k, None)
    num_entries = len(results['ids'][0])    
    for i in range(num_entries):
        entry = {}
        for key, values in results.items():
            entry[key] = values[0][i]
        transformed_list.append(entry)  
    return transformed_list

async def main():
    
    # Populate the search results panel
    @ui.refreshable
    async def populate() -> None:
        results = []
        query = search.value
        if query:    
            results = await run.cpu_bound( get_results, query,  5)
            if results:
                ui.label('Results').style('font-size: 125%').classes('bg-slate-300 w-full')
                for entry in results:
                    formatted_timestamp = format_timestamp( entry['metadatas']['timestamp'] )
                    vid = entry['metadatas']['video']
                    youtube_url = f"https://www.youtube.com/watch?v={vid}&t={formatted_timestamp}"
                    title = entry['metadatas']['title']
                    with ui.row().classes('border-2 border-slate-600 p-2 items-center mt-2 hover:bg-amber-100'):
                        ui.image(f"https://img.youtube.com/vi/{vid}/hqdefault.jpg").style('width: 240px;')
                        with ui.column().style().classes().style('width: 320px;'):
                            ui.link(f"{title} ({formatted_timestamp})", youtube_url, new_tab=True).classes('text-pretty').style('font-size: 115%;')
                            ui.space()
                            ui.label("..."+entry['documents']+"...").style('font-size: 115%; font-style: italic')
    
    # Build the UI
    with ui.row().classes('w-full gap-2'):
        with ui.column().classes().style():
            ui.label(f'Search {COLLECTION_NAME}').style('font-size: 125%').classes('w-full text-center bg-slate-300')
            with ui.row():
                search = ui.input(label='enter search terms').props('rounded outlined dense clearable').style('font-size: 125%; width: 500px;')
                ui.button(icon='search', on_click=populate.refresh)
            ui.label('  ')
            await populate()
    
if __name__ in {"__main__", "__mp_main__"}:    
    ui.run(title='YTTS')




