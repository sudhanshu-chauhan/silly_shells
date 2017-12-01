import os
import sys

import psycopg2
import ConfigParser


def main():
    try:
        config_file_path = os.environ.get('CONFIG_FILE_PATH')
        postgres_db_params = {}
        print('configuring silly shells server...')
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
        connection.close()


    except Exception as error:
        print(error.message)
        sys.exit(1)
