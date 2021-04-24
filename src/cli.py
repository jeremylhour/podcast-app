"""Command Line Interface for the app

Usage:
    podcast ls
    podcast lastep <podcast_name>
    podcast stop
          
"""
from docopt import docopt

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
        print(', '.join(podcasts))
    
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
            while player.is_playing() == 1:
                continue
            stopListening(newEpisode, player)
    
    if args['stop']:
        pass

if __name__=='__main__':
    pass