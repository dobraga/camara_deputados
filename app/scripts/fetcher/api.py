import requests
import json
import os

def transform_where(where):
    url = ''

    for i, key in enumerate(where.keys()):
        if i > 0:
            url += '&'

        url += key + '=' + where[key]

    return(url)

def read_json(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)

    return data

class Api:
    def __init__(self, ctx):
        self.url = ctx.url
        self.input = ctx.input_dir
        self.querys = read_json(ctx.querys)

    def request(self, query):
        name = query + '.jsonl'

        self.take(query)
        self.save(name)

    def take(self, query):
        query = self.querys[query]

        grupo = query['from'].split('.')
        nivel = len(grupo)

        if nivel > 2:
            print('Existe acesso apenas até o segundo nível')
            return False

        self.url += '/{grupo}'.format(grupo = grupo[0])
        
        if 'where' in query.keys():
            where = query['where']

            if 'id' in where.keys():
                id = where['id']

                self.url += '/{id}'.format(id = id)

                if nivel == 1:
                    return True

                else:
                    self.url += '/{subgrupo}'.format(subgrupo = grupo[1])
                    del where['id']

            else:
                if nivel == 2:
                    print('Para acessar os valores do segundo nível é nescessário que utilize o filtro de ID')
                    return False

            where = transform_where(where)

            self.url += '?{where}'.format(where = where)

            return True
        
        if nivel == 2:
            print('Para acessar os valores do segundo nível é nescessário que utilize o filtro de ID')
            return False

    def save(self, name):
        req = requests.get(self.url)
        dados = req.json()['dados']

        if isinstance(dados, list):
            with open(os.path.join(self.input, name), 'w', encoding='utf-8') as f:
                for line in dados:
                    json.dump(line, f, ensure_ascii=False)
                    f.write("\n")

        else:
            with open(os.path.join(self.input, name), 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False)