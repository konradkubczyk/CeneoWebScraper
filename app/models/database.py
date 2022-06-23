import yaml
import mysql.connector
import app.database_schema as database_schema

class Database():
    def __init__(self):
        with open('config.yml', 'r') as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
            self.username = config['db']['username']
            self.password = config['db']['password']
            self.port = config['db']['port']
            self.hostname = config['db']['hostname']
            self.database = database_schema.DB_NAME
            self.tables = database_schema.TABLES
        self.initialize_database()

    def initialize_database(self):
        connection = self.connect()
        cursor = connection.cursor()
        query = f"CREATE DATABASE IF NOT EXISTS {self.database} DEFAULT CHARACTER SET 'utf8';"
        cursor.execute(query)
        connection.database = self.database
        for table_name in self.tables:
            table_description = self.tables[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
        cursor.close()
        connection.close()
        print("Database ready.")

    def connect(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                user=self.username,
                passwd=self.password,
                host=self.hostname,
                port=self.port
            )
            print("MySQL connection successful.")
        except mysql.connector.Error as err:
            print(f"Error: '{err}'")
        return connection