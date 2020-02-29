import sys
sys.path.append('/app/scripts/deputados/')
from sqlengine import SQLEngine
from reader import create_filename, read_sql

import os
import logging
import pandas as pd

class Loader:
    def __init__(self, conf):
        self.sqlengine = SQLEngine(conf)
        self.input = conf.input_dir
        self.sql_dir = conf.sql_dir
        self.file_map = {
            'partidos_det': 'partidos',
            'deputados': 'deputados'
        }

    def create_commands(self, type, ds_nodash, ds, file):
        commands = []
        if type in self.file_map.keys():
            table = self.file_map[type]
        else:
            raise('Arquivo sem mapeamento com tabela')

        commands.append(read_sql(os.path.join(self.sql_dir, 'ddl', table+'.sql')))

        commands.append('DROP TABLE IF EXISTS tbl_{table}_{ds_nodash}_stg;')
        commands.append('CREATE TABLE tbl_{table}_{ds_nodash}_stg (dados jsonb);')

        commands.append('COPY tbl_{table}_{ds_nodash}_stg FROM \'{file}\';')
        commands.append('DROP TABLE IF EXISTS tbl_{table}_{ds_nodash};')
        commands.append('CREATE TABLE tbl_{table}_{ds_nodash}() INHERITS(tbl_{table});')

        commands.append(read_sql(os.path.join(self.sql_dir, 'dml', table+'.sql')))
        commands.append('DROP TABLE tbl_{table}_{ds_nodash}_stg;')

        return [command.format(table = table, ds_nodash = ds_nodash, ds = ds, file = file) for command in commands]

    def load(self, type, ds_nodash, ds):
        file = create_filename(self.input, type, ds_nodash)
        commands = self.create_commands(type, ds_nodash, ds, file)

        for command in commands:
            self.sqlengine.execute(command)

        os.remove(file)


def load(file, conf, **context):
    loader = Loader(conf)
    loader.load(file, context['ds_nodash'], context['ds'])
