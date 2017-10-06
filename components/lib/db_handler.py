import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import (User,
                    SecurityCredential,
                    ClientMachine,
                    ClientProcess)
from conf.settings import DATABASE_URL
from logger import Logger


logger_params = {
    'file_name': 'error.log',
    'file_handler': True,
    'stream_handler': False
}
logger_instance = Logger(**logger_params)


class HandleDB:
    """HandleDB class for handling db interactions.
    """

    def __init__(self):
        """
        HandleDB __init__ method.
        """
        try:
            self.engine = create_engine(DATABASE_URL)
            Session = sessionmaker(bind=self.engine)

            self.session_instance = Session()
        except Exception as error:
            logger_instance.logger.error(
                'HandleDB::__init__:{}'.format(error.message))

    def create_user(self, **user_params):
        """Create User method for HandleDB class

        Args:
            user_params (Dict): Parameters for User object creation.

        """
        try:
            user_params['uuid'] = str(uuid.uuid4())
            current_user = User(**user_params)
            self.session_instance.add(current_user)
            self.session_instance.commit()
            return current_user
        except Exception as error:
            logger_instance.logger.error(
                'HandleDB::create_user:{}'.format(error.message))
            return False

    def update_user(self, user_id, **user_params):
        """Update User method for HandleDB."""
        try:
            self.session_instance.query(User).filter_by(
                uuid=user_id).update(**user_params)
            self.session_instance.commit()
            return self.session_instance.query(
                User).filter_by(uuid=user_id).first()

        except Exception as error:
            logger_instance.logger.error(
                'HandleDB::update_user:{}'.format(
                    error.message))
            return None

    def create_security_credential(self, **secureity_credential_params):
        """Create Security Credential method for HandleDB Class.

        Args:
            security_credential_params (Dict): multi key, value param
            for security credential object creation.

        """
        try:
            secureity_credential_params['uuid'] = str(uuid.uuid4())
            security_credential_instance = SecurityCredential(
                **secureity_credential_params
            )
            self.session_instance.add(security_credential_instance)
            self.session_instance.commit()
            return security_credential_instance

        except Exception as error:
            logger_instance.logger.error(
                'HandleDB::create_security_credential:{}'.format(
                    error.message
                ))
            return False

    def update_security_credential(self,
                                   security_credential_id,
                                   **security_credential_params):
        """Update Security Credential method for HandleDB class."""
        try:
            self.session_instance.query(
                SecurityCredential).filter_by(
                uuid=security_credential_id).update(
                **security_credential_params)
            self.session_instance.commit()
            return self.session_instance.query(
                SecurityCredential).filter_by(
                uuid=security_credential_id).first()

        except Exception as error:
            logger_instance.logger.error(
                'HandleDB::update_security_credentials:{}'.format(
                    error.message))
            return None

    def create_client_machine(self, **client_machine_params):
        """Create Client Machine method for HandleDB Class."""
        try:
            client_machine_params['uuid'] = str(uuid.uuid4())
            client_machine_instance = ClientMachine(**client_machine_params)
            self.session_instance.add(client_machine_instance)
            self.session_instance.commit()
            return client_machine_instance
        except Exception as error:
            logger_instance.logger.error(
                'HandleDB::create_client_machine:{}'.format(
                    error.message))
            return None

    def update_client_machine(self,
                              client_machine_id,
                              **client_machine_params):
        """Update Client Machine method for HandleDB class."""
        try:
            self.session_instance.query(
                ClientMachine).filter_by(
                uuid=client_machine_id).update(**client_machine_params)
            self.session_instance.commit()
            return self.session_instance.query(
                ClientMachine).filter_by(
                uuid=client_machine_id).first()

        except Exception as error:
            logger_instance.logger.error(
                'HandleDB::update_client_machine:{}'.format(
                    error.message))
            return None

    def create_client_process(self, **client_process_params):
        """Create Client Process method for HandleDB class."""
        try:
            client_process_params['uuid'] = str(uuid.uuid4())
            client_process_instance = ClientProcess(**client_process_params)
            self.session_instance.add(client_process_instance)
            self.session_instance.commit()
            return client_process_instance

        except Exception as error:
            logger_instance.logger.error(
                'HandleDB::create_client_process:{}'.format(
                    error.message))
            return None

    def update_client_process(self,
                              client_process_id,
                              **client_process_params):
        """Update Client Process method for HandleDB class."""
        try:
            self.session_instance.query(
                ClientProcess).filter_by(uuid=client_process_id).update(
                **client_process_params)
            self.session_instance.commit()
            return self.session_instance.query(
                ClientProcess).filter_by(uuid=client_process_id).first()

        except Exception as error:
            logger_instance.logger.error(
                'HandleDB::update_client_process:{}'.format(
                    error.message))
            return None