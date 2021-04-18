#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database management tools
Here, the database is used to save all the podcasts that have been read

Created on Sun Apr 11 21:53:42 2021

@author: jeremylhour
"""
import os

from tinydb import TinyDB, Query


def getDataBase(db_dir='.database/'):
    """
    getDataBase:
        gets the database,
        and creates the database if it does not exists
    
    @param output_dir (str): directory where the database is located
    """
    # Create dir
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    database = TinyDB(db_dir+'read_episodes.json')
    return database

if __name__=='__main__':
    pass