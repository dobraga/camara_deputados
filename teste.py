from app.scripts.fetcher.api import Api
from app.scripts.utils import Setings

conf = Setings()

api = Api(conf)

api.request('partidos')
