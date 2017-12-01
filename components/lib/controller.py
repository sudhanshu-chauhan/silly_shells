import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User, SecurityCredential
from db_handler import HandleDB
from logger import Logger

logger_instance_params = {
    'file_name': 'error.log',
    'stream_handler': True,
    'file_handler': True}
logger_instance = Logger(**logger_instance_params)


database_url = 'postgresql://postgres:random123@localhost/silly_shells'
engine = create_engine(database_url)
session_instance = sessionmaker(bind=engine)()


class UserController:

    def __init__(self):
        pass

    @staticmethod
    def authenticate(email, password):
        try:
            query_result = session_instance.query(
                User).filter(User.email == email)
            if query_result.count() == 0:
                return False
            param_password_hash = hashlib.md5(password).hexdigest()
            db_password_hash = session_instance.query(SecurityCredential).get(
                query_result.one().security_credential).password_hash
            if param_password_hash == db_password_hash:
                return True
            else:
                return False
        except Exception as error:
            logger_instance.logger.error(
                'UserController::authenticate:{}'.format(error.message))
            return False


class ClientMachineController:
    def __init__(self):
        pass

    @staticmethod
    def create_client_machine(**client_params):
        try:
            hdb_instance = HandleDB()
            client_machine = hdb_instance.create_client_machine(
                **client_params)
            if client_machine is not None:
                return client_machine.id
            else:
                raise Exception('could not create client machine...')

        except Exception as error:
            logger_instance.logger.error(
                'ClientMachineController::create_client_machine:{}'.format(
                    error.message))
            return None
