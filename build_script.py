# -*- coding: utf-8 -*-
"""
Created on Wed May  1 12:48:18 2024


"""

# Script for generating our local ytts database

from chroma import build_db
from videos import word_chunk_generator

chan_name = 'MrCarlsonslab'
config = {'channel_name': chan_name,
          'collection_name': 'word_chunk_20_15',
          'path': "Z:/ytts_db",
          'chunk': 20,
          'adv_by': 15,
          'chunk_func':  word_chunk_generator
          }

build_db(**config)


chan_name = 'Thesignalpath'
config = {'channel_name': chan_name,
          'collection_name': 'word_chunk_20_15',
          'path': "Z:/ytts_db",
          'chunk': 20,
          'adv_by': 15,
          'chunk_func': word_chunk_generator
          }
          
build_db(**config)
          
          
