import sys
sys.path.append('/home/dobraga/Desktop/camara_deputados/app/scripts/deputados/')

from deputados.api import Api
from deputados.settings import Settings
from deputados.sqlengine import SQLEngine

conf = Settings()
api = Api(conf)

#api.request('partidos_membros')

sql = SQLEngine(conf)

sql.execute('partidos.sql')