import sys
sys.path.append('/app/scripts/deputados/')
from reader import read_yaml

import os
import yaml
from airflow.models import Variable

workdir = os.path.abspath(os.path.join( __file__ , '..', '..', '..'))

with open(os.path.join(workdir,'settings','settings.yml'), 'r') as stream:
    conf = yaml.safe_load(stream)

def _get(attribute):
    return conf[attribute]

class Settings():
    def __init__(self, query_file = 'extract.json'):
        self.url = _get('url')
        self.workdir = workdir
        self.input_dir = os.path.join(workdir, 'input')
        self.settings_dir = os.path.join(workdir, 'settings')
        self.sql_dir = os.path.join(workdir, 'sql')
        self.fetch_retry = _get('fetch_retry')

        self.querys = read_yaml(os.path.join(self.settings_dir, 'extract.json'))
        self.postgres_host = _get('postgres_host')
        self.postgres_database = _get('postgres_database')
        self.postgres_user = _get('postgres_user')
        self.postgres_password = _get('postgres_password')
