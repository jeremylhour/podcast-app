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
from src import DB_DIR, DB_FILE

def getDataBase(db_dir=DB_DIR, db_file=DB_FILE):
    """
    getDataBase:
        gets the database,
        and creates the database if it does not exists
    
    @param db_dir (str): directory where the database is located
    @param db_file (str): name of the .json file where the db is saved
    
    Both these parameters are specified in the __init__
    """
    # Create dir
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    database = TinyDB(db_dir+db_file)
    return database

if __name__=='__main__':
    pass