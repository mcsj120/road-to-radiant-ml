import psycopg2 as pg
import json

class databaseConnecter:

    def __init__(self):
        with open('./config.json') as f:
            data = json.load(f)
            self.connection = pg.connect(
                user=data.user,
                password=data.password,
                host=data.host,
                port=data.port,
                database=data.database
            )

        self.cursor = self.connection.cursor()
        print(self.connection.get_dsn_parameters(),"\n")
    
        #Display the PostgreSQL version installed
        self.cursor.execute("SELECT version();")
        record = self.cursor.fetchone()
        print("You are connected into the - ", record,"\n")

    def query(self, string):
        self.cursor.execute(string)
        return self.cursor.fetchall()