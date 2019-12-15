from app.scripts.utils.sqlengine import SQLEngine
import os
import logging

class Loader:
    def __init__(self, ctx):
        self.sqlengine = SQLEngine()
        self.input = ctx.input_dir

    def load_file(self, table, file):
        file = os.path.join(self.input, file)

        command = 'LOAD DATA INFILE "{file}" INTO TABLE {table};'.format(file = file, table = table)

        logging.warning(command)

        return self.sqlengine.execute(command)
