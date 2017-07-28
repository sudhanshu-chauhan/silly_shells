import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import User


database_url = 'postgresql://postgres:random123@localhost/silly_shells'
engine = create_engine(database_url)

Session = sessionmaker(bind=engine)


class HandleDB:
    """
    HandleDB class for handling db interactions.
    """

    def __init__(self):
        """
        HandleDB __init__ method.
        """
        pass

    def create_user(self, **user_params):
        """Create User method for HandleDB class

        Args:
            user_params (Dict): Parameters for User object creation.

        """
        try:
            user_params['uuid'] = str(uuid.uuid4())
            current_user = User(**user_params)
            session_instance = Session()
            session_instance.add(current_user)
            session_instance.commit()
            return True
        except Exception as error:
            print(error.message)
            return False
