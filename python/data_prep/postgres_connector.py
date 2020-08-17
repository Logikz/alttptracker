import pandas
import psycopg2

import config_reader


class PostgresConnector:

    def __init__(self):
        self.connection = None

    @property
    def _connection(self):
        if not self.connection:
            self.connect_to_db()
        return self.connection

    def connect_to_db(self):
        """
        Connects to the Link to the Past Randomizer Stats DB
        :return: Connection to postgres table
        """
        self.connection = None
        try:
            config = config_reader.read_config('database.ini', 'postgres')

            print("Attempting to connect to db...")
            self.connection = psycopg2.connect(**config)
            print("Connection established")
        except Exception as e:
            print(e)
            exit(1)

    def execute_sql(self, sql_statement):
        """
        Runs a sql command and loads it into a pandas dataframe for manipulation
        :param sql_statement: String
        :return: Pandas Dataframe
        """
        return pandas.read_sql_query(sql_statement, self.connection)

    def cleanup(self):
        if not self.connection:
            self.connection.cursor().close()
            self.connection.close()
