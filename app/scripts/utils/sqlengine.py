import MySQLdb

class SQLEngine:
    def __init__(self):
        self.mydb = MySQLdb.connect(
            host='db',
            user='root',
            passwd='123',
            db='deputados'
        )

        self.cursor = self.mydb.cursor()

    def execute(self, command):
        return self.cursor.execute(command)