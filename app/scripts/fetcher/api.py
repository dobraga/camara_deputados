from ..utils.reader import read_json, read_jsonl
from datetime import datetime
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

class Api:
    def __init__(self, ctx):
        self.url = ctx.url
        self.input = ctx.input_dir
        self.querys = read_json(ctx.querys)
        self._already_run = 0

    def request(self, query, dt_ini = None, dt_fim = None):
        self.take(query)
        name = query + '.jsonl'
        file = os.path.join(self.input, name)

        with open(file, 'w') as f:
            dep = self.querys[query]['id'] if 'id' in self.querys[query].keys() else None
            dt_ini = dt_ini or datetime.now().strftime('%Y-%m-%d')
            dt_fim = dt_fim or datetime.now().strftime('%Y-%m-%d')

            if dep:
                self.url = self.url.format(id= '{id}', dataInicio = dt_ini, dataFim = dt_fim)
                dep = read_jsonl(os.path.join(self.input, dep) + '.jsonl')

                for line in dep:
                    if line['id']:
                        url = self.url.format(id = line['id'])
                        self.save(f, url)

            self.save(f)

    def take(self, query):
        if self._already_run == 0:
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
                    del where['id']

                    if nivel == 2:
                        self.url += '/{subgrupo}'.format(subgrupo = grupo[1])

                where = transform_where(where)

                self.url += '?{where}'.format(where = where)
            
            elif nivel == 2:
                print('Para acessar os valores do segundo nível é nescessário que utilize o filtro de ID')
                return False

            self._already_run = 1
            return True

    def save(self, file, url = None):
        req = requests.get(url or self.url)

        auxs = req.json()['links']
        links = []

        if len(auxs) == 1:
            links.append(auxs[0]['href'])
        else:
            for aux in auxs:
                if aux['rel'] != 'self':
                    links.append(aux['href'])

        links = list(set(links))

        for link in links:
            req = requests.get(link)            
            dados = (req.json()['dados'])

            if 'ultimoStatus' in dados.keys():
                del dados['ultimoStatus']

            if isinstance(dados, list):
                for line in dados:
                    json.dump(line, file, ensure_ascii=False)
                    file.write("\n")

            else:
                json.dump(dados, file, ensure_ascii=False)
                file.write("\n")
