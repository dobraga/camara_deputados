import os
import yaml

dir = os.path.split(__file__)[0]
dir = os.path.join(dir, '..', '..')

with open(os.path.join(dir,'settings','settings.yml'), 'r') as stream:
    conf = yaml.safe_load(stream)

def _get(attribute):
    return conf[attribute]

class Setings():
    def __init__(self):
        self.workdir = dir
        self.input_dir = os.path.join(self.workdir, 'input')
        self.querys = os.path.join(self.workdir, 'settings', 'extract.json')
        self.url = _get('url')
