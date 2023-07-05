import configparser as cp
import os
import pandas as pd
import requests as re
import sqlalchemy
import mysql.connector
from sqlalchemy import text

class Extractor:

    def __init__(self):
        '''
            Al generarse una instancia de la clase Extractor, se genera una conexión al MySQL.
        '''
        
        config = cp.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), 'config', 'settings.ini'))

        mysqlurl = "mysql+mysqlconnector://"+config.get('MySQLInstance','MYSQL_ROOT_USER')+":"+config.get('MySQLInstance','MYSQL_ROOT_PASSWORD') \
                    +"@"+config.get('MySQLInstance','MYSQL_IP')+":"+config.get('MySQLInstance','MYSQL_PORT')+"/"+config.get('MySQLInstance','MYSQL_DATABASE')

        self.engine = sqlalchemy.create_engine(mysqlurl)
        self.connection = self.engine.connect()
        

    def getDataFromEndpoint(self,endpoint):
        '''
            Retorna un pandas dataframe con los datos provenientes de un endpoint y con formato csv.
        '''

        return pd.read_csv(endpoint)
    
    def getMySQLConnection(self):
        return self.connection
    
    def run_MySQL_query(self, query):
        '''
            Ejecuta la query pasada como parámetro en la base de MySQL y la commitea.
        '''

        self.connection.execute(text(query))
        self.connection.commit()
    
    def rollback_MySQL_connection(self):
        self.connection.rollback()

    def disposeMySQLConnection(self):
        self.engine.dispose()

    def closeMySQLConnection(self):
        self.connection.close()
    



