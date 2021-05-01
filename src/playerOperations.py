#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Player operations:
    defines the player operations
Created on Sun Apr 11 21:11:14 2021

@author: jeremylhour
"""
import yaml
import feedparser
import time
from datetime import datetime

import vlc

from src.podcastClasses import Podcast, Episode

# -------------------------------------- 
# Functions to manage podcast and time,
# including updating the databse
# --------------------------------------

def stopListening(episode, player):
    """
    stopListening:
        stop listening to the podcast and update the episode timestamp accordingly

    @param podcast (Episode):
    @param player (vlc.MediaPlayer):
    """
    stopTime = player.get_time()
    if player.is_playing()==1:
        player.stop()
    episode.updateTimestamp(stopTime)
    episode.saveToDataBase()
    return None

def resumeListening(episode, player):
    """
    resumeListening:
        resume listening to the episode

    @param podcast (Episode):
    @param player (vlc.MediaPlayer):
    """
    if player.is_playing()==0:
        player.play()
    player.set_time(episode.timestamp)
    print(f'Duration of the episode : {player.get_length()}')
    time.sleep(2) # to give time to let the player resume
    return None

def jumpTime(player, jump=30):
    """
    jumpTime:
        jump in episode time

    @param player (vlc.MediaPlayer):
    @param jump (int): a time jump, in seconds
    """
    if player.is_playing()==1:
        currentTime = player.get_time()
        player.set_time(currentTime + jump*1000)
    else:
        print('The podcast is not playing.')
    return None

# -------------------------------------- 
# Utils
# --------------------------------------

def msToHMS(duration : int):
    """
    msToHMS:
        convert given to duration to a H:M:S format
    
    @param duration (int): duration to be converted
    """
    seconds = int((duration/1000)%60)
    minutes = int((duration/(1000*60))%60)
    hours = int((duration/(1000*60*60))%24)
    return f"{hours}:{minutes}:{seconds}"


if __name__=='__main__':
    config_file = 'subscriptions.yml'
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
        
    podcast = Podcast(config['subscriptions']['Flagrant 2'])
    history = podcast.getLastEpisode()
    
    newEpisode = next(history)
    newEpisode.displayInfos()
    print(newEpisode.audioUrl)
    
    # Play the podcast
    player = vlc.MediaPlayer(newEpisode.audioUrl)
    resumeListening(newEpisode, player)
    print(player.get_time())
    time.sleep(10)

    """
    player.set_time(15830)
    time.sleep(5)
    
    stopListening(newEpisode, player)
    resumeListening(newEpisode, player)
    
    jumpTime(player, jump=30)
    time.sleep(10)
    """