import json
import yaml

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
