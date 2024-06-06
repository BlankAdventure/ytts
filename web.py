# -*- coding: utf-8 -*-
"""

Created on Wed Apr 17 22:34:56 2024

@author: Patrick
"""

from nicegui import ui, run
import chromadb


class Overlay(ui.element):
    def __init__(self, message, bg_color=(0,0,0,0.5)):
        super().__init__(tag='div')
        self.message = message
        self.style('position: fixed; display: block; width: 100%; height: 100%;'
                   'top: 0; left: 0; right: 0; bottom: 0; z-index: 2; cursor: pointer;'
                   'background-color:' + f'rgba{bg_color};')
        with self:
            with ui.element('div').classes("h-screen flex items-center justify-center"):
                ui.label(self.message).style("font-size: 50px; color: white;")
        self.hide()

    def show(self):
        self.set_visibility(True)
    
    def hide(self):
        self.set_visibility(False)


# Converts timestamp returned by query into more use-friendly string
def format_timestamp(timestamp: float) -> str:
    hours = int(timestamp / 3600)
    minutes = int((timestamp % 3600) / 60)
    seconds = int(timestamp % 60)
    return f"{hours}h{minutes}m{seconds}s"

# Issue a querty to the database and return (cleaned up) results
def get_results(collection, qstr: str, n=5) -> list[dict]:
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


async def main(em: callable, channel_name: str, db_name: str, db_path: str=None) -> None:
    
    # Load db from persistent media location if db_path specfied
    # otherwise connect to server (running locally)
    if db_path:
        client = chromadb.PersistentClient(path=db_path)
    else: # 
        client = chromadb.HttpClient(host="localhost", port=8000)
    collection = client.get_collection(name=db_name, embedding_function=em)
    
    # Populate the search results panel
    @ui.refreshable
    async def populate() -> None:
        results = []
        query = search.value
        if query:    
            overlay.show()
            results = await run.io_bound(get_results,collection, query, 5)
            overlay.hide()
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
    overlay = Overlay('Searching. Please be patient.')
    with ui.row().classes('w-full gap-2'):
        with ui.column().classes().style():
            ui.label(f'Search {channel_name}').style('font-size: 125%').classes('w-full text-center bg-slate-300')
            with ui.row():
                search = ui.input(label='enter search terms').props('rounded outlined dense clearable').style('font-size: 125%; width: 500px;')
                ui.button(icon='search', on_click=populate.refresh)
            ui.label('  ')
            await populate()


if __name__ in {"__main__", "__mp_main__"}:
    @ui.page('/a')
    async def testa():
        await (main('MrCarlsonsLab','MrCarlsonslab', db_path='Z:/ytts_db'))

    @ui.page('/b')
    async def testb():
        await (main('TheSignalPath','Thesignalpath', db_path='Z:/ytts_db'))

    ui.run(title='YTTS')




