# -*- coding: utf-8 -*-
"""
Created on Wed May  1 12:48:18 2024


"""

# Script for generating our local ytts database

from chroma import build_db


chan_name = 'MrCarlsonslab'
config = {'channel_name': chan_name,
          'collection_name': chan_name,
          'path': "./",
          'chunk': 6,
          'adv_by': 4
          }

build_db(**config)


chan_name = 'Thesignalpath'
config = {'channel_name': chan_name,
          'collection_name': chan_name,
          'path': "./",
          'chunk': 6,
          'adv_by': 4
          }
          
build_db(**config)
          
          
