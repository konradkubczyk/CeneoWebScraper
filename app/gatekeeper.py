import os
from app.models.database import Database

def launch():
    if not os.path.exists("config.yml"):
        answer = ""
        no_database = False
        docker = False
        print("No configuradion file detected, commencing interactive configurator...")
        print("Access to a MySQL database is required for data storage.")
        while answer not in ["y", "n"]:
            answer = input("Do you have a database you wish to use? [y/n] ")
        if answer == "n":
            no_database = True
            answer = ""
            while answer not in ["y", "n"]:
                answer = input("Do you want to generate a stack.yml file to launch a new MySQL instance using Docker? [y/n] ")
            if answer == "y":
                docker = True
                print("Ok, the stack.yml file will be generated.")
            else:
                print("Please provision a new MySQL database and relaunch the app.")
                exit()
        print("Please provide MySQL database connection details:")
        username = "root"
        if not docker:
            username = input(" - username: ")
        password = input(" - password: ")
        hostname = "localhost"
        if not docker:
            hostname = input(" - hostname: ")            
        port = input(" - port: ")
        print("Saving config.yml...", end="")
        with open(f"config.yml", "w", encoding="UTF-8") as cfile:
            cfile.write(f"db:\n  username: {username}\n  password: {password}\n  hostname: {hostname}\n  port: {port}")
        print(" Done.")
        if no_database:
            print("Saving stack.yml...", end="")
            with open(f"stack.yml", "w", encoding="UTF-8") as sfile:
                sfile.write(f"version: '3.1'\n\nservices:\n  db:\n    image: mysql\n    environment:\n      MYSQL_ROOT_PASSWORD: {password}\n    ports:\n      - \"{port}:3306\"")
            print(" Done.")
            print("Please provision the new database using 'docker compose -f stack.yml up' in the main directory of the app and relaunch the app when the server will be ready for connections.")
            print("If you would like to run the configurator again, please delete the config.yml file.")
            exit()
    Database().initialize_database()
