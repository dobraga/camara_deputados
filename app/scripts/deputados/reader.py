import json
import yaml
import os

def read_json(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
    return data

def read_jsonl(file):
    data = []
    with open(file, 'r') as json_file:
        for line in json_file:
            data.append(json.loads(line))
    return data

def read_yaml(file):
    with open(file, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data

def read_sql(file):
    with open(file, 'r') as sql_file:
        sql = sql_file.read()
    return ' '.join(sql.split())

def create_filename(input, file, ds=None):
    if ds:
        filename = '{}_{}.jsonl'.format(file, ds)
    else:
        filename = file + '.jsonl'

    return os.path.join(input, filename)