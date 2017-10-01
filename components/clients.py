import json

import websocket
import requests as rq
from ConfigParser import ConfigParser

from lib.logger import Logger


client_config_path = './client_config.cfg'
config_instance = ConfigParser()
config_instance.read(client_config_path)

logger_instance = Logger(**{
    'file_name': 'error.log',
    'log_dir': config_instance.get('settings', 'log_dir'),
    'stream_handler': True,
    'file_handler': True,
})

logger_instance_info = Logger(**{
    'file_name': 'client.log',
    'log_dir': config_instance.get('settings', 'log_dir'),
    'file_handler': False,
    'stream_handler': True
})


class Client:

    def __init__(self, server=None, port=80, https_enabled=False):
        try:
            if server is None:
                raise Exception('server ip address not provided')
                self.auth_api_endpoint = 'get_token/'
                self.server = server
                self.port = port
                if https_enabled:
                    self.api_protocol = 'https'
                else:
                    self.api_protocol = 'http'
        except Exception as error:
            logger_instance.logger.error(
                'Client::__init__:{}'.format(error.message))

    def get_token(self, **credential):
        try:
            if 'email' not in credential or 'password' not in credential:
                raise Exception('invalid credential param')
            auth_url = '{}://{}:{}/{}'.format(self.api_protocol,
                                              self.server,
                                              self.port,
                                              self.auth_api_endpoint)

            response = rq.post(auth_url, data=json.dumps(credential))
            if response.status_code == 200:
                return response.json()['token']
            else:
                return None

        except Exception as error:
            logger_instance.logger.error(
                'Client::get_token:{}'.format(error.message))
            return None

    def set_token(self, token):
        """set_token method to set token in config file."""
        try:
            config_instance.set('client', 'token', token)
            return True
        except Exception as error:
            logger_instance.logger.error(
                'Client::set_token:{}'.format(error.message))
            return False


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### client closed ###")


def on_open(ws):
    logger_instance_info.logger.info('opened socket connection')

if __name__ == '__main__':
    client_instance = Client(server='192.168.16.37', port=8001)
    credential_param = {'email': 'sudhanshu@radiowalla.in',
                        'password': 'testg'}
    header = {'Authorization': client_instance.get_token(**credential_param)}
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('ws://localhost:8001/sock_server/',
                                header=header,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
