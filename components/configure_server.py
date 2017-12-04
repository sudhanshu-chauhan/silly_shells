import os
import sys

import psycopg2
from ConfigParser import ConfigParser
from lib import models

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

MAX_SERVER_DELAY = 10  # server timeout value in microseconds


def main():
    try:
        config_file_path = os.environ.get('SERVER_CONFIG_FILE_PATH')
        config_instance = ConfigParser()
        if not os.path.exists(config_file_path):
            print('configuration file not found...exiting')
            sys.exit(1)

        config_instance.read(config_file_path)
        postgres_db_params = {}
        print('configuring silly shells server...')
        print('checking mongodb server...')
        mongo_client = MongoClient(serverSelectionTimeoutMS=MAX_SERVER_DELAY)
        mongo_client.server_info()
        print('configuring postgres db params')

        postgres_db_params['host'] = str(
            raw_input('enter postgres db server host'))
        postgres_db_params['user'] = str(
            raw_input('enter postgresql user name'))
        postgres_db_params['port'] = int(
            raw_input('enter postgres db server port'))
        postgres_db_params['dbname'] = str(
            raw_input('enter target database name'))
        postgres_db_params['password'] = str(
            raw_input('enter password for target db'))

        print('checking postgresql database params...')
        connection = psycopg2.connect(**postgres_db_params)
        print('postgresql params verification successful!')
        print('Creating database and models...')
        cursor = connection.cursor()
        cursor.execute('create database {}'.format(
            postgres_db_params['dbname']))
        cursor.close()
        connection.close()
        models.Base.metadata.create_all(models.engine)
        print('Database models created successfully!')

    except ServerSelectionTimeoutError as mongo_error:
        print('mongodb server error: {}'.format(mongo_error.message))
        print('server configuration failed. exiting ...')
        sys.exit(1)

    except Exception as error:
        print(error)
        sys.exit(1)


if __name__ == '__main__':
    main()
