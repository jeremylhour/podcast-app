#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define the podcast objects

Created on Sat Apr 10 21:10:06 2021

@author: jeremylhour
"""
import yaml
import feedparser
import time
from datetime import datetime

from tinydb import Query

from src.database import getDataBase

# --------------------------
# Object classes definitions
# --------------------------

class Podcast():
    """
    Podcast:
        Podcast object, created from url of the RSS feed
    """

    def __init__(self, url):
        """
        init the object and directly parse the url

        @param url (str): url for the RSS feed of the podcast
        """
        self.url = url
        self.feed = feedparser.parse(self.url)
        self.title = self.feed.feed.get('title')

    def getLastEpisode(self):
        """
        getLastEpisode:
            A generator to get the last episode, goes from most recent to older.
            Queries the latest timestamp from the database.
        """
        for feedEntry in self.feed.entries:
            publishedDate = datetime.fromtimestamp(time.mktime(feedEntry.published_parsed))
            podcastEpisode = Episode(
                podcastName=self.title,
                title=feedEntry['title'],
                date=publishedDate,
                summary=feedEntry['summary'],
                audioUrl=_extractAudioUrl(feedEntry)
                )
            podcastEpisode.loadFromDataBase()
            yield podcastEpisode


class Episode():
    """
    Episode:
        A class for episodes from a podcast
    """
    def __init__(self, podcastName, title, date, summary, audioUrl):
        """
        @param podcastName (str): title of the podcast
        @param title (str): title of the episode
        @param date (datetime.datetime): date of publication
        @param summary (str): summary of the podcast
        @param audiorUrl (str): url to the audio file
        """
        self.podcastName = podcastName
        self.title = title
        self.date = date
        self.summary = summary
        self.audioUrl = audioUrl
        self.timestamp = 0

    def displayInfos(self):
        """
        displayInfos:
            print episode infos to the screen
        """
        print('\n')
        print(f'Title : \n {self.title}')
        print(f'Date : \n {self.date.strftime("%d %b %Y, %H:%M")}')
        print(f'Summary : \n {self.summary} \n')

        db = getDataBase()
        User = Query()
        result = db.get(User.audioUrl == self.audioUrl)
        if result is None:
            print(">> This is a new episode.")

    def toDict(self):
        """
        toDict:
            passes arg to dict, so it can be saved to database
        """
        dico = {
            'podcastName': self.podcastName,
            'title': self.title,
            'date': self.date.strftime("%d/%m/%Y, %H:%M:%S"),
            'audioUrl': self.audioUrl,
            'timestamp': self.timestamp
            }
        return dico

    def loadFromDataBase(self):
        """
        loadFromDataBase:
            check if the episode already exists in the database,
            and if so, loads the correct timestamp.
        """
        db = getDataBase()
        User = Query()
        result = db.get(User.audioUrl == self.audioUrl)
        if result is not None:
            self.updateTimestamp(result['timestamp'])
        return None

    def saveToDataBase(self):
        """
        saveToDataBase:
            save the current episode to database
        """
        db = getDataBase()
        dico = self.toDict()
        User = Query()
        db.upsert(dico, User.audioUrl == self.audioUrl) # audioUrl is the key of the database

    def updateTimestamp(self, newTimestamp):
        """
        updateTimestamp:
            update the Timestamp when the podcast stops playing

        @param newTimestamp (int): new starting time
        """
        self.timestamp = newTimestamp

    def resetTimestamp(self):
        """
        resetTimestamp:
            reset the timestamp
        """
        self.timestamp = 0


# -------
# Utils
# -------

def _extractAudioUrl(feedEntry):
    """
    extractAudioUrl:
        extract the url of the audio episode from the feed entry

    @param feedEntry (dict): a dict that might have an url linking to an audio
    """
    for link in feedEntry['links']:
        if 'audio' in link['type']:
            audioLink = link['href']
    return audioLink


if __name__=='__main__':
    print("="*80)
    print("THIS IS A TEST")
    print("="*80)

    config_file = 'subscriptions.yml'
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)

    url = config['subscriptions']['Flagrant 2']
    podcast = Podcast(url)
    print(f'The current podcast is: {podcast.title}')
    history = podcast.getLastEpisode()

    print('Here is the most recent episode')
    newEpisode = next(history)
    newEpisode.displayInfos()

    print('Here is the second most recent episode')
    newEpisode2 = next(history)
    newEpisode2.displayInfos()