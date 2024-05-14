# YouTube Transcript Search

[Live Demo 1 - Mr Carlson's Lab](http://www.blankadventure.com/ytts1)

[Live Demo 2 - The Signal Path](http://www.blankadventure.com/ytts2)

(_Each database was built with a chunk size of 6 and an overlap of 2._)

YTTS is an exploration of enabling semantic search capabilities on a YouTube channel. The idea was initially sparked by Mr. Carlson Lab, whose videos are a deep-dive into antique electronics repair. His videos are information-dense and I would often find myself wishing I could remember some clever method or technqiue for circuit debugging, noise reduction, or performance testing. The ability to semantically search his content for various topcis seemed like exactly the thing I needed, and so this is my attempt. 

A few things would be needed to accomplish this: (1) scraping the channel for video transcripts; (2) transforming the transcripts; (3) storing to a database; and (4) enabling the search.


(1) Scraping the channel for video transcripts

Thankfully, YT provides transcripts for (most of?) their videos, so we don't have to actually generate those. Two packages were used: scrapetube and youtube_transcript_api, whose functionality was combined in videos.py to enable collecting a set of transcripts for a YT channel.

(2) Transforming the transcripts

The transcript for a single video consists of a list of dictionaries, where each dictionary contains a single (text) sentence and a start and end timestamp. It's important to note that each "sentence" is really just a string of some number of words, and isn't necessarily a sentence in the proper grammatical sense. Because of this, the contextual value of a particular sentence may be limited. To improve context, we can append multiple sentences together forming larger text samples. Additionally, a rolling-window aggregator can be used to provide "overlapped" (or shared) context between samples. The appropriate start timestamp must be maintained across this operation (the end timestamp is not used). The transcript does not include the video title, which is obtained separately, and is inserted as an addtional piece of metadata. In videos.py, chunk_generator handles this functionality. It is a generator that yields a single sample in the form:

```python
{'text': 'its a Panasonic radio receiver that winds up like a clock then it searches for radio stations lets do a tear down on this Ill do a circuit description then lets fix it and see how this mechanism actually works should be a lot of fun lets get started heres the Panasonic radar mtic radio that were going to be tearing down troubleshooting and were going to',
 'metadata': {'timestamp': 4.319,
  'title': 'Panasonic Radar Matic Receiver Teardown With Circuit Description, Troubleshooing, And Resurrection!',
  'video': '6B_-WznDq1g'},
 'uid': '6B_-WznDq1g_0'
}
```

These samples are then subsequently added to our database of choice.


(3) Storing to a database

The current implemenation relies on chromadb (https://www.trychroma.com/), an open-source embeddings database. The code at present uses the default all-MiniLM-L6-v2 model, but chromadb wraps a variety of other LLMs as well (TBD: try some others!).




