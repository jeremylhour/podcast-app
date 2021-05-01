__version__ = '1.0.0'

# ------------------------------------------
# DATABASE CONFIG
#   used in database.py
# ------------------------------------------
import yaml

CONFIG_FILE = '../subscriptions.yml'
with open(CONFIG_FILE, 'r') as stream:
    config = yaml.safe_load(stream)

DB_DIR = config['DB_DIR']
DB_FILE = config['DB_FILE']