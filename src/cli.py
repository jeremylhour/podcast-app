"""Command Line Interface for the app

Usage:
    podcast ls
    podcast lastep <podcast_name>
    podcast stop
          
"""
from docopt import docopt

import os
import sys
import yaml
import vlc
import time

from src.podcastClasses import Podcast, Episode
from src.playerOperations import stopListening, resumeListening, jumpTime

def main():
    args = docopt(__doc__)

    # Load podcast list :
    config_file = 'subscriptions.yml'
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)

    if args['ls']:
        podcasts = list(config['subscriptions'].keys())
        print('You are subscribed to the following podcasts :')
        print(', \n'.join(podcasts))
    
    if args['lastep']:
        url = config['subscriptions'].get(args['<podcast_name>'])
        if url is not None:
            podcast = Podcast(url)
            print(f'You have selected : {podcast.title}')
            history = podcast.getLastEpisode()

            # New episode
            newEpisode = next(history)
            newEpisode.displayInfos()
            player = vlc.MediaPlayer(newEpisode.audioUrl)
            resumeListening(newEpisode, player)
            try:
                while player.is_playing() == 1:
                    continue
                stopListening(newEpisode, player)
            except KeyboardInterrupt:
                stopListening(newEpisode, player)
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)

    if args['pastep']:
        url = config['subscriptions'].get(args['<podcast_name>'])
        
    if args['stop']:
        pass

if __name__=='__main__':
    pass