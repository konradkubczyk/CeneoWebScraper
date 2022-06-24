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

    def initialize_database(self):
        cnx = self.connect()
        cursor = cnx.cursor()
        query = f"CREATE DATABASE IF NOT EXISTS {self.database} DEFAULT CHARACTER SET 'utf8';"
        cursor.execute(query)
        cnx.database = self.database
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
                print("done.")
        cursor.close()
        cnx.close()
        print("Database ready.")

    def connect(self):
        cnx = None
        try:
            cnx = mysql.connector.connect(
                user=self.username,
                passwd=self.password,
                host=self.hostname,
                port=self.port
            )
            print("MySQL connection successful.")
        except mysql.connector.Error as err:
            print(f"Error: '{err}'")
            exit()
        return cnx
    
    def execute_query(self, query, data=None):
        cnx = self.connect()
        cnx.database = self.database
        cursor = cnx.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
        print(f"Query executed: {query}")

