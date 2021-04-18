"""Command Line Interface for the app

Usage:
    commands.py ls
          
"""
from docopt import docopt

import yaml

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


if __name__=='__main__':
   main()