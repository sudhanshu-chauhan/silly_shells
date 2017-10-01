import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User, SecurityCredential
from logger import Logger

logger_instance_params = {
    'file_name': 'error.log',
    'stream_handler': True,
    'file_handler': True
}
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
                query_result.one().security_credential
            ).password_hash
            if param_password_hash == db_password_hash:
                return True
            else:
                return False
        except Exception as error:
            logger_instance.logger.error(
                'UserController::authenticate:{}'.format(error.message))
            return False


class ClientController:
    """ClientController class to deal with client information exchange."""

    def __init__(self):
        pass

    def get_client_stats(self):
        """method to get client cpu/memorh usage."""
        # code goes here

    def get_process_stats(self, pid):
        """method to get stat of process running at client side."""
        # code goes here

    def reboot_client(self):
        """method to reboot remote client."""
        # code goes here

    def get_camera_shot(self):
        """method to get camera shot of the remote client machine."""
        # code goes here

    def get_client_details(self):
        """method to fetch client details of remote machine."""
        # code goes here
