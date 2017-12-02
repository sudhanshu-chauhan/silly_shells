import json

from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler
from tornado.web import Application, RequestHandler
import jwt

from lib.logger import Logger
from lib.controller import UserController, ClientMachineController
from lib.db_handler import HandleDB
from lib.conf import settings

logger_instance = Logger(**{
    'file_name': 'error.log',
    'stream_handler': True,
    'file_handler': True})
logger_instance_info = Logger(**{
    'file_name': 'tornado_server.log',
    'stream_handler': True,
    'file_handler': False})


active_clients = []
hdb_instance = HandleDB()


class SocketOutputHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        try:
            token = self.request.headers.get('Authorization')
            payload = jwt.decode(token, verify=False)

            if 'email' not in payload:
                self.close()
            client_params = {}
            client_params['secret_websocket_key'] = self.request.headers.get(
                'Sec-Websocket-Key')
            client_params['client_id'] = self.request.headers.get('client_id')
            active_client_id = hdb_instance.add_active_client(**client_params)
            if active_client_id is None:
                print('could not activate client!')
                self.close()
            else:
                print('client activated: {}'.format(active_client_id))

            if self not in active_clients:
                active_clients.append(self)
        except jwt.exceptions.DecodeError as error:
            self.close()

        except Exception as error:
            logger_instance.logger.error(
                'SocketOutputHandler::open:{}'.format(
                    error.message))

    def on_message(self, message):
        try:
            logger_instance_info.logger.info('client message::{}'.format(
                message))
        except Exception as error:
            logger_instance.logger.error(
                'SocketOutputHandler::on_message:{}'.format(error.message))

    def on_close(self):
        try:
            logger_instance_info.logger.info(
                'disconnecting client...')
        except Exception as error:
            logger_instance.logger.error(
                'SocketOutputHandler::on_close:{}'.format(error.message))

    def authenticate_client(self):
        try:
            pass
        except Exception as error:
            logger_instance.logger.error(
                'SocketOutputHandler::authenticate_client:{}'.format(
                    error.message))


class ClientAuthentication(RequestHandler):

    def post(self, *args, **kwargs):
        try:
            post_param = json.loads(self.request.body)
            if 'email' not in post_param or 'password' not in post_param:
                raise KeyError

            if UserController.authenticate(post_param['email'],
                                           post_param['password']):
                payload = {
                    'email': post_param['email'],
                    'password': post_param['password']}
                response_json = {'token': jwt.encode(
                    payload, settings.JWT_SECRET, algorithm='HS512')}
                self.write(json.dumps(response_json))
            else:
                self.clear()
                self.set_status(403)
                self.write('<html><body>invalid credentials</body></html>')

        except Exception as error:
            logger_instance.logger.error(
                'ClientAuthentication::post:{}'.format(error.message))


class Machine(RequestHandler):
    """Machine class to create/list machine instances."""

    def post(self, *args, **kwargs):
        """Post method to accept params and create a machine instance."""
        try:
            post_param = json.loads(self.request.body)
            token = self.request.headers.get('Authorization')
            token_payload = jwt.decode(token, verify=False)
            if 'email' in token_payload:
                machine_id = ClientMachineController.create_client_machine(
                    **post_param)
                if machine_id is not None:
                    self.clear()
                    self.set_status(201)
                    self.write(machine_id)
                else:
                    self.clear()
                    self.set_status(500)
                    self.write('<html><body>server error: 500</body></html>')
            else:
                self.clear()
                self.set_status(403)
                self.write('<html><body>invalid token</body></html>')

        except Exception as error:
            logger_instance.logger.error(
                'Machine::post:{}'.format(error.message))


class MainApplication(Application):

    def __init__(self):
        handlers = [
            (r'/sock_server/', SocketOutputHandler),
            (r'/get_token/', ClientAuthentication),
            (r'/create_machine/', Machine)]

        Application.__init__(self, handlers)


def main():
    app_instance = MainApplication()
    print('[*] started socket server at 8001')
    app_instance.listen(8001, address='0.0.0.0')
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
