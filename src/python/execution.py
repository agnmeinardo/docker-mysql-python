import configparser as cp
import os
import extractor as ext
import logging
import sys


def getData():

    '''
        Función que devuelve el dataframe creado por la instancia de la clase Extractor a la cual se le pasó como parámetro
        la URL del endpoint pertinente.
    '''

    logging.info("Retrieving data from API.")

    config = cp.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config', 'settings.ini'))
    url = config.get('Endpoint','Url')

    return extractor.getDataFromEndpoint(url)

def copyToTempTable():

    '''
        Función que copia los datos del dataframe hacia la tabla temporal temp_users.
    '''

    logging.info("Copying the data from csv to temporary table.")

    extractor.run_MySQL_query('DROP TEMPORARY TABLE IF EXISTS temp_users;')

    extractor.run_MySQL_query('CREATE TEMPORARY TABLE IF NOT EXISTS temp_users SELECT * FROM users LIMIT 0;')

    data_read.to_sql('temp_users',con=extractor.engine,if_exists='replace',index=False)

    logging.info("Data has been copied into temporary table.")

def updateUsersByExistingID():

    '''
        Función que hace un update de los usuarios que se vieron modificados a partir del ID existente desde el archivo origen.
    '''

    logging.info("Updating data modified for existing users.")

    query = """ UPDATE users u 
                INNER JOIN temp_users tu ON tu.id = u.id
                SET u.first_name = tu.first_name,
                    u.last_name = tu.last_name,
                    u.email = tu.email,
                    u.gender = tu.gender,
                    u.ip_address = tu.ip_address,
                    u.uploaded_date = CURRENT_TIMESTAMP(6)
                where tu.first_name <> u.first_name
                or tu.last_name <> u.last_name
                or tu.email <> u.email
                or tu.gender <> u.gender
                or tu.ip_address <> u.ip_address;
            """
    
    extractor.run_MySQL_query(query)

    logging.info("Data modified for existing users.")

def deleteByExistingEmail():

    '''
        Función que elimina los usuarios que vienen con el mismo mail, pero distinto ID desde el archivo origen.
    '''

    logging.info("Deleting users with existing email but different id. The new id will be inserted in the next step.")

    query = """ DELETE FROM users WHERE id IN (SELECT id FROM 
                (SELECT DISTINCT u.id AS id FROM users u, temp_users tu
                WHERE u.id <> tu.id AND u.email = tu.email) AS e);"""
    
    extractor.run_MySQL_query(query)

    logging.info("Data deleted for existing emails but different id.")
    

def insertNewUsers(): 
    '''
        Función que inserta los nuevos usuarios y los que tenían ID nuevo para un mail ya existente en la tabla users.
    '''

    logging.info("Inserting new records into users table.")

    query = """ INSERT INTO users (SELECT tu.*, CURRENT_TIMESTAMP(6) FROM temp_users tu 
                LEFT JOIN users u ON tu.id = u.id AND tu.email = u.email
                WHERE u.id IS NULL);"""
    
    extractor.run_MySQL_query(query)

    logging.info("New data was inserted into users table.")



def main():

    global extractor, data_read

    logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), 'log', 'execution.log'),
                        filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    logging.info("The execution has started.")

    logging.info("Trying to connect to MySQL database.")

    try:

        extractor = ext.Extractor()
        extractor.getMySQLConnection()

    except Exception as e:

        logging.error("Extractor could not be generated.")
        logging.error(str(e))
        sys.exit(1)

    try:
        
        data_read = getData()

    except Exception as e:

        logging.error("Data could not be retrieve from endpoint.")
        logging.error(str(e))
        sys.exit(1)

    try:
        copyToTempTable()

        deleteByExistingEmail()

        updateUsersByExistingID()

        insertNewUsers()

        extractor.closeMySQLConnection()

        extractor.disposeMySQLConnection()

        logging.info("The execution has finished.")
        

    except Exception as e:
        
        logging.error("An error has occurred.")
        logging.error(str(e))

        extractor.rollback_MySQL_connection()
        extractor.closeMySQLConnection()
        extractor.disposeMySQLConnection()
        sys.exit(1)


main()
