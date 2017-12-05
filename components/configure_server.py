import os
import sys
import hashlib
import getpass

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from ConfigParser import ConfigParser
from lib import models
from lib.db_handler import HandleDB

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

MAX_SERVER_DELAY = 10  # server timeout value in microseconds
hdb_instance = HandleDB()


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

        # mongodb instance check
        print('checking mongodb server...')
        mongo_client = MongoClient(serverSelectionTimeoutMS=MAX_SERVER_DELAY)
        mongo_client.server_info()
        print('mongodb status OK')

        # setting up postgresql database and models
        print('configuring postgres db params')
        postgres_db_params['host'] = str(
            raw_input('enter postgres db server host: '))
        postgres_db_params['user'] = str(
            raw_input('enter postgresql user name: '))
        postgres_db_params['port'] = int(
            raw_input('enter postgres db server port: '))
        postgres_db_name = str(
            raw_input('enter target database name: '))
        postgres_db_params['password'] = str(
            getpass.getpass('enter password for target db: '))

        print('checking postgresql database params...')
        connection = psycopg2.connect(**postgres_db_params)
        print('Postgresql status OK')
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print('postgresql params verification successful!')
        print('Creating database and models...')
        cursor = connection.cursor()
        cursor.execute('create database {}'.format(
            postgres_db_name))
        cursor.close()
        connection.close()
        models.Base.metadata.create_all(models.engine)
        print('Database models created successfully!')
        print('creating super user...')
        superuser_params = {}
        superuser_params['first_name'] = str(
            raw_input('enter super user first name: '))
        superuser_params['last_name'] = str(
            raw_input('enter super user last name: '))
        superuser_params['email'] = str(raw_input('enter super user email: '))
        password_hash = hashlib.md5(getpass.getpass(
            'enter super user password: ')).hexdigest()
        credential_param = {'password_hash': password_hash}
        credential_instance = hdb_instance.create_security_credential(
            **credential_param)
        superuser_params['security_credential'] = credential_instance.uuid
        if hdb_instance.create_superuser(**superuser_params):
            print('super user created successfully!')
        else:
            print('error in creating super user... exiting')
            sys.exit(1)
        print('Server Configuration Successful! Adios!')

    except ServerSelectionTimeoutError as mongo_error:
        print('mongodb server error: {}'.format(mongo_error.message))
        print('server configuration failed. exiting ...')
        sys.exit(1)

    except Exception as error:
        print(error)
        sys.exit(1)


if __name__ == '__main__':
    main()
