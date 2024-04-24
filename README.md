YTTS is an exploration of enabling semantic search capabilities on a YouTube channel. The idea was initially sparked by Mr. Carlson Lab, whose videos are a deep-dive into antique electronics repair. His videos are information-dense and I would often find myself wishing I could remember some clever method or technqiue for circuit debugging, noise reduction, or performance testing. The ability to semantically search his content for various topcis seemed like exactly the thing I needed, and so this is my attempt. 

A few things would be needed to accomplish this: (1) scraping the channel for video transcripts; (2) transforming the transcripts; (3) storing to a database; and (4) enabling the search.


(1) Scraping the channel for video transcripts

Thankfully, YT provides transcripts for (most of?) their videos, so we don't have to actually generate those. Two packages were used: scrapetube and youtube_transcript_api, whose functionality was combined in videos.py to enable collecting a set of transcripts for a YT channel.

(2) Transforming the transcripts

The transcript for a single video consists of a list of dictionaries, where each dictionary contains a single (text) sentence and a start and end timestamp. It's important to note that each "sentence" is really just a string of some number of words, and isn't necessarily a sentence in the proper grammatical sense. Because of this, the conextual value of a particular sentence may be limited. To improve context, we can append multiple sentences together forming larger text samples. Additionally, a rolling-window aggregator can be used to provide "overlapped" (or shared) context between samples. The appropriate start timestamp must be maintained across this operation (the end timestamp is not used). The transcript does not include the video title, which is obtained separately, and is inserted as an addtional piece of metadata. In videos.py, chunk_generator handles this functionality. It is a generator that yields a single sample in the form:


(3) Storing to a database

The current implemenation relies on chromadb.
