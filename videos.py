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

def add_to_db(vid_ids, collection):
    failed = []
    for vid in tqdm(vid_ids):
        print(f'*** Video: {vid} ***')        
        title = get_video_metadata(vid)['title'] #for now we only care about the title
        transcript = get_transcript(vid)    
        if transcript:
            count = 0
            for entry in tqdm(transcript):
                text = entry['text']
                metadata = {'timestamp': entry['start'], 'title': title, 'video': vid}
                uid = f'{vid}_{count}'
                collection.add(documents=[text], metadatas=[metadata], ids=[uid])
                count += 1
        else:
            failed.append(vid)
    return failed

# Get list of all videos in a channel
def get_video_ids(channel: str ="MrCarlsonsLab") -> list[str]:
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

# Get total time of list of vids 
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
        
# Get transcript from a given video ID
def get_transcript(vid_id: str) -> dict:
    transcript = None
    try:
        transcript = YouTubeTranscriptApi.get_transcript(vid_id)
    except Exception as e:
        print(e)
    return transcript
       
# Convert transcript (list of dicts featuring sub-strings) into single
# (unbroken) text string. All metadata is discarded!
def get_text(vid_id: str, strip: bool = True) -> str:
    transcript = YouTubeTranscriptApi.get_transcript(vid_id)
    text = TextFormatter().format_transcript(transcript)
    if strip:
        text = [s for s in text.replace("\n"," ") if s.isalnum() or s.isspace()]
        text = "".join(text)
    return text


