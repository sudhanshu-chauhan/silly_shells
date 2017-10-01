import json

from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler
from tornado.web import Application, RequestHandler
import jwt

from lib.logger import Logger
from lib.controller import UserController
from lib.conf import settings

logger_instance = Logger(**{
    'file_name': 'error.log',
    'stream_handler': True,
    'file_handler': True
})
logger_instance_info = Logger(**{
    'file_name': 'tornado_server.log',
    'stream_handler': True,
    'file_handler': False
})


active_clients = []


class SocketOutputHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        try:
            token = self.request.headers.get('Authorization')
            payload = jwt.decode(token, verify=False)

            if 'email' not in payload:
                self.close()

            if self not in active_clients:
                active_clients.append(self)
        except jwt.exceptions.DecodeError as error:
            self.close()

        except Exception as error:
            logger_instance.logger.error(
                'SocketOutputHandler::open:{}'.format(
                    error.message
                ))

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
            logger_instance


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
                    'password': post_param['password']
                }
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


class MainApplication(Application):

    def __init__(self):
        handlers = [
            (r'/sock_server/', SocketOutputHandler),
            (r'/get_token/', ClientAuthentication),
        ]

        Application.__init__(self, handlers)


def main():
    app_instance = MainApplication()
    print('[*] started socket server at 8001')
    app_instance.listen(8001, address='0.0.0.0')
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
