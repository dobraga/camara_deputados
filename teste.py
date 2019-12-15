from app.scripts.fetcher.api import Api
from app.scripts.utils import Setings
from app.scripts.utils.loader import Loader

conf = Setings()
api = Api(conf)
load = Loader(conf)

api.request('partidos')
#api.request('partidos_membros')
#api.request('deputados')

load.load_file('deputados.tbl_partidos_stg', 'partidos.jsonl')