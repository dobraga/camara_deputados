import sys
sys.path.append('/app/scripts/deputados/')

import os
import psycopg2
import logging

class SQLEngine:
    def __init__(self, conf, executor = 'dml'):
        self.path = os.path.join(conf.sql_dir, executor)
       
        self.db = psycopg2.connect(
            host=conf.postgres_host,
            user=conf.postgres_user,
            password=conf.postgres_password,
            database=conf.postgres_database
        )

    def execute(self, command = None):
        if command:
            logging.info(command)

            with self.db.cursor() as cursor:
                ret = cursor.execute(command)
                self.db.commit()
                return ret
        else:
            raise("Precisa de algum comando para executar essa função")