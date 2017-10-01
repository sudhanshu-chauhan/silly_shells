from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column,
                        String,
                        Text,
                        DateTime,
                        ForeignKey)
from sqlalchemy import create_engine


Base = declarative_base()
database_url = 'postgresql://postgres:random123@localhost/silly_shells'
engine = create_engine(database_url)


class User(Base):
    """
    User class for user model.
    """
    __tablename__ = "user"

    uuid = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    security_credential = Column(String,
                                 ForeignKey('security_credential.uuid'),
                                 nullable=False)


class SecurityCredential(Base):
    """
    SecureityCredentials model class to security creds for user.
    """
    __tablename__ = "security_credential"

    uuid = Column(String, primary_key=True)
    password_hash = Column(String)


class ClientMachine(Base):
    """
    ClientMachine class model for storing machine information.
    """
    __tablename__ = "client_machine"

    uuid = Column(String, primary_key=True)
    name = Column(String)
    description = Column(Text)
    mac_address = Column(String)
    public_ip = Column(String)
    internal_ip = Column(String)
    last_active = Column(DateTime)


class ClientProcess(Base):
    """
    ClientProcess class model for storing client's process information.
    """
    __tablename__ = "client_process"

    uuid = Column(String, primary_key=True)
    name = Column(String)
    path = Column(String)
    interpreter_path = Column(String)
    status = Column(String)
    last_active = Column(DateTime)
