# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:28:03 2024

@author: BlankAdventure
"""
import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import urllib.request
import json
import urllib
from tqdm import tqdm
from math import ceil

tqdm._instances.clear()


# Chunks together transcript rows into buff_len, and advances by adv_by. 
# buff_len: number of sentences to combine
# adv_by: number of sentences to advancy by (think sliding window)
def chunk_generator(vid_ids: list[str], buff_len: int, adv_by: int) -> dict | None:
    NV = len(vid_ids)
    def get_chunk(a, b):
        buffer = transcript[a:b]    
        text = get_text(buffer)
        metadata = {'timestamp': buffer[0]['start'], 'title': title, 'video': vid}
        uid = f'{vid}_{start}'
        return {'text': text, 'metadata': metadata, 'uid': uid}

    for n, vid in enumerate(vid_ids):
        start = 0
        stop = buff_len 
        title = get_video_metadata(vid)['title'] #for now we only care about the title
        transcript = get_transcript(vid)  
        if transcript:
            NT = len(transcript)
            P = ceil( (NT-buff_len)/adv_by )
            pbar = tqdm(total=P,desc=f'{vid} ({n+1}/{NV})')
            while stop < NT:
                yield get_chunk(start, stop)
                start += adv_by
                stop += adv_by
                pbar.update(1)
            # Need to get any leftovers...
            yield ( get_chunk(start,NT) )
            pbar.update(1)
            pbar.close()                
        else:
            yield None


# Returns a generator yielding either a dictionary containing the transcript text, 
# metadata and unique ID, OR, None if unable to load. 
def entry_generator(vid_ids: list[str]) -> dict | None:
    N = len(vid_ids)
    for n, vid in enumerate(vid_ids):
        title = get_video_metadata(vid)['title'] #for now we only care about the title
        transcript = get_transcript(vid)    
        if transcript:
            count = 0
            for entry in tqdm(transcript, f'{vid} ({n+1}/{N})'):
                text = entry['text']
                metadata = {'timestamp': entry['start'], 'title': title, 'video': vid}
                uid = f'{vid}_{count}'
                count += 1
                yield {'text': text, 'metadata': metadata, 'uid': uid}
        else:
            yield None

# Get list of all videos in a channel
def get_video_ids(channel: str) -> list[str]:
    videos = scrapetube.get_channel(channel_username=channel)
    vid_ids = [video['videoId'] for video in videos]
    return vid_ids


# Retrieves video metadata (title key probably of most interest)
def get_video_metadata(vid_id: str) -> dict:
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % vid_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
    return data 

# Helper function - get total time of list of vids 
def total_length(vid_ids: list[str]) -> tuple[list[float], list[str]]:
    all_ends = []
    failed = []
    n = len(vid_ids)
    for idx, vid_id in enumerate(vid_ids):
        print(f'Processing {vid_id} ({idx}/{n})')
        transcript = get_transcript(vid_id)
        if transcript:
            last_entry = transcript[-1]['start'] #IN SECONDS!!
            all_ends.append(last_entry)
        else:
            print('> FAILED. Skipping.')
            failed.append(vid_id)
    return all_ends, failed
        
# Get transcript from a given video ID. Returns None if unable to load.
def get_transcript(vid_id: str) -> dict | None:
    transcript = None
    try:
        transcript = YouTubeTranscriptApi.get_transcript(vid_id)
    except Exception as e:
        print(e)
    return transcript
       
# Convert transcript (list of dicts featuring sub-strings) into single
# (unbroken) text string. All metadata is discarded!
def get_text(transcript: list[dict], strip: bool = True) -> str:
    text = TextFormatter().format_transcript(transcript)
    if strip:
        text = [s for s in text.replace("\n"," ") if s.isalnum() or s.isspace()]
        text = "".join(text)
    return text


