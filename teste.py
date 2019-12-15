from app.scripts.fetcher.api import Api
from app.scripts.utils import Setings

conf = Setings()

api = Api(conf)

#print(api.take('deputados'))

#print(api.url)

#api.request('partidos')
#api.request('partidos_membros')
api.request('deputados')

#from app.scripts.utils.reader import read_jsonl

#print(read_jsonl('/home/dobraga/Desktop/camara_deputados/app/input/partidos.jsonl'))