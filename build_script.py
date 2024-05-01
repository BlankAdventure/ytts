# -*- coding: utf-8 -*-
"""
Created on Wed May  1 12:48:18 2024


"""

# Script for generating our two local ytts databases

from chroma import build_db


chan_name = 'MrCarlsonslab'
config = {'channel_name': chan_name,
          'db_name': chan_name,
          'path': "./",
          'chunk': 8,
          'adv_by': 5
          }

build_db(**config)


chan_name = 'Thesignalpath'
config = {'channel_name': chan_name,
          'db_name': chan_name,
          'path': "./",
          'chunk': 6,
          'adv_by': 4
          }
          
build_db(**config)
          
          
