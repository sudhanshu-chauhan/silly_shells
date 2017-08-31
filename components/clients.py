import json

import websocket
import requests as rq

from lib.logger import Logger

logger_instance = Logger(**{
    'file_name': 'error.log',
    'stream_handler': True,
    'file_handler': True,
})

logger_instance_info = Logger(**{
    'file_name': 'client.log',
    'file_handler': False,
    'stream_handler': True
})


class Client:

    def __init__(self, auth_url=None):
        self.auth_url = auth_url

    def get_token(self, **credential):
        try:
            if 'email' not in credential or 'password' not in credential:
                raise Exception('invalid credential param')
            if self.auth_url is None:
                raise Exception('authentication url not provided.')

            response = rq.post(self.auth_url, data=json.dumps(credential))
            if response.status_code == 200:
                return response.json()['token']
            else:
                return None

        except Exception as error:
            logger_instance.logger.error(
                'Client::get_token:{}'.format(error.message))
            return None


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### client closed ###")


def on_open(ws):
    logger_instance_info.logger.info('opened socket connection')

if __name__ == '__main__':
    client_instance = Client(auth_url='http://localhost:8001/get_token/')
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
