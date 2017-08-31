import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import (User,
                    SecurityCredential)


database_url = 'postgresql://postgres:random123@localhost/silly_shells'
engine = create_engine(database_url)

Session = sessionmaker(bind=engine)


class HandleDB:
    """HandleDB class for handling db interactions.
    """

    def __init__(self):
        """
        HandleDB __init__ method.
        """
        self.session_instance = Session()

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
            print('HandleDB::create_user:{}'.format(error.message))
            return False

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
            print('HandleDB::create_security_credential:{}'.format(
                error.message
            ))
            return False
