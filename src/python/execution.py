import configparser as cp
import os
import extractor as ext
import logging


def getData():

    logging.info("Retrieving data from API.")

    config = cp.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config', 'settings.ini'))
    url = config.get('Endpoint','Url')

    return extractor.getDataFromEndpoint(url)

def copyToTempTable():

    logging.info("Copying the data from csv to temporary table.")

    extractor.run_MySQL_query('DROP TABLE IF EXISTS temp_users;')

    extractor.run_MySQL_query('CREATE TABLE IF NOT EXISTS temp_users SELECT * FROM users LIMIT 0;')

    data_read.to_sql('temp_users',con=extractor.engine,if_exists='replace',index=False)

    logging.info("Data has been copied into temporary table.")

def updateUsersByExistingID():

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

    logging.info("Deleting users with existing email but different id. The new id will be inserted in the next step.")

    query = """ DELETE FROM users WHERE id IN (SELECT id FROM 
                (SELECT DISTINCT u.id AS id FROM users u, temp_users tu
                WHERE u.id <> tu.id AND u.email = tu.email) AS e);"""
    
    extractor.run_MySQL_query(query)

    logging.info("Data deleted for existing emails but different id.")
    

def insertNewUsers(): # Se insertan los nuevos y los que tenían un ID nuevo pero con mail ya existente que fueron borrados en el paso anterior
    logging.info("Inserting new records into users table.")

    query = """ INSERT INTO users (SELECT tu.*, CURRENT_TIMESTAMP(6) FROM temp_users tu 
                LEFT JOIN users u ON tu.id = u.id AND tu.email = u.email
                WHERE u.id IS NULL);"""
    
    extractor.run_MySQL_query(query)

    logging.info("New data was inserted into users table.")



def main():

    global extractor, data_read, logger

    logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), 'log', 'execution.log'),
                        filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    logging.info("The execution has started.")

    logging.info("Trying to connect to MySQL database.")
    extractor = ext.Extractor()
    extractor.getMySQLConnection()

    try:
        data_read = getData()

        copyToTempTable()

        deleteByExistingEmail()

        updateUsersByExistingID()

        insertNewUsers()

        extractor.closeMySQLConnection()

        extractor.disposeMySQLConnection()

        logging.info("The execution has finished.")
        

    except Exception as e:

        logger.error("ERROR: " + str(e))

        extractor.closeMySQLConnection()
        
        extractor.disposeMySQLConnection()


main()
