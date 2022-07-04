import pyodbc
from db_credentials import sqlserver_db_config as db_source
from db_credentials import postgres_db_config as db_dest
from sqlalchemy import create_engine

def sqlserver_conection():
    #Conectarse a la  Base de Datos SqlServer 2019
        connection_string = f'DRIVER={db_source["driver"]};SERVER={db_source["server"]};DATABASE={db_source["database"]};UID={db_source["user"]};PWD={db_source["password"]};TrustServerCertificate=yes;'
        connection = pyodbc.connect(connection_string)
        return connection


def postgres_conection():
    #Conectarse a una base de datos Postgres
    engine = create_engine(f'postgresql://{db_dest["user"]}:{db_dest["password"]}@{db_dest["server"]}:{db_dest["port"]}/{db_dest["database"]}')
    engine.connect()
    return engine

        