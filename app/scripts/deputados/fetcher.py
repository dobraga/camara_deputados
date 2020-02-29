import sys
sys.path.append('/app/scripts/deputados/')
from reader import read_json, read_jsonl, create_filename

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from datetime import datetime
import multiprocessing as mp
from time import sleep
import requests
import logging
import json
import os

N = mp.cpu_count()

def transform_where(where):
    url = ''

    for i, key in enumerate(where.keys()):
        if i > 0:
            url += '&'

        url += key + '=' + where[key]

    return(url)

class Fetcher:
    def __init__(self, conf):
        self.url = conf.url
        self.input = conf.input_dir
        self.querys = conf.querys
        self.fetch_retry = conf.fetch_retry

    def _requests_retry_session(self, backoff_factor=2, status_forcelist=(500, 502, 503, 504)):
        sleep(0.01)
        session = requests.Session()
        retry = Retry(total=self.fetch_retry, read=self.fetch_retry, connect=self.fetch_retry, backoff_factor=backoff_factor, status_forcelist=status_forcelist)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def save(self, file, url):
        try:
            req = self._requests_retry_session().get(url)

            auxs = req.json()['links']           
            links = set()

            if len(auxs) == 1:
                links.add(auxs[0]['href'])
            else:
                for aux in auxs:
                    if aux['rel'] != 'self':
                        links.add(aux['href'])

            with open(file, 'a') as file:
                for link in links:
                    req = self._requests_retry_session().get(link)            
                    dados = (req.json()['dados'])

                    if isinstance(dados, dict):
                        dados = [dados]
                    
                    for line in dados:
                        line['urlBase'] = link
                        json.dump(line, file, ensure_ascii=False)
                        file.write("\n")
        
        except Exception:
            logging.error('Error in fetch %s', url)
            raise ValueError('Error in fetch data')

class Api(Fetcher):
    def __init__(self, conf):
        super().__init__(conf)
        self.querys = self.querys['API']

    def request(self, query, context):
        url = self.create_url(query)
        url = url.format(id= '{id}', dataInicio = context['yesterday_ds'], dataFim = context['ds'])
        logging.info(url)
        
        path_file = create_filename(self.input, query, context['ds_nodash'])
        logging.info(path_file)

        if os.path.exists(path_file):
            os.remove(path_file)

        dependencia = self.querys[query]['id'] if 'id' in self.querys[query].keys() else None

        if dependencia:
            dep_file = read_jsonl(create_filename(self.input, dependencia, context['ds_nodash']))

            ls_url = [url.format(id = line['id']) for line in dep_file if line['id']]
            ls_pool = [(path_file, url) for url in ls_url]

            logging.info(ls_url)

            with mp.Pool(processes = N) as p:
                results = p.starmap(self.save, ls_pool)
                
        else:
            self.save(path_file, url)

    def create_url(self, query):
        url = self.url
        query = self.querys[query]

        grupo = query['from'].split('.')
        nivel = len(grupo)

        if nivel > 2:
            raise 'Existe acesso apenas até o segundo nível'

        url += '/{grupo}'.format(grupo = grupo[0])
        
        if 'where' in query.keys():
            where = query['where']

            if 'id' in where.keys():
                url += '/{id}'
                del where['id']

                if nivel == 2:
                    url += '/{subgrupo}'.format(subgrupo = grupo[1])
                    
            elif nivel == 2:
                raise 'Para acessar os valores do segundo nível é nescessário que utilize o filtro de ID'

            where = transform_where(where)

            url += '?{where}'.format(where = where)

        return url

def extrai(query, conf, **context):
    api = Api(conf)
    return api.request(query, context)
