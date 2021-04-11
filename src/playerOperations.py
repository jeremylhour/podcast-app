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

from podcastClasses import Podcast, Episode

# -------------------------------------- 
# Functions to manage podcast and time
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
    episode.timestamp = stopTime
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
    return None


if __name__=='__main__':
    config_file = 'subscriptions.yml'
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
        
    for podcast in config['subscriptions']:
        print(podcast)
        url = config['subscriptions'][podcast]
        
    podcast = Podcast(url)
    history = podcast.getLastEpisode()
    
    newEpisode = next(history)
    
    # Play the podcast
    player = vlc.MediaPlayer(newEpisode.audioUrl)
    player.play()
    player.get_time()
    player.set_time(15830)
    
    stopListening(newEpisode, player)
    resumeListening(newEpisode, player)
    
    jumpTime(player, jump=30)