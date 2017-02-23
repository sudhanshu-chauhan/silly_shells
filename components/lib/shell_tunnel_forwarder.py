import getpass
import os
import socket
import select
import sys
import threading
from optparse import OptionParser

import paramiko

SSH_PORT = 22
DEFAULT_PORT = 4000
PKEY_PASSPHRASE = None
g_verbose = True


class ShellTunnelForwarder():
    """ShellTunnelForwarder class."""

    def __init__(self):
        """Instantiate ShellTunnelForwarder class."""
        pass

    @staticmethod
    def reverse_socket_handler(channel,
                               host,
                               port):
        r"""Handler for reverse socket connection.

        :param channel: remote connection transport object\
         (type paramiko.transport.Transport)
        :param host: remote address (type str)
        :param port: remote port (type int)
        """
        socket_obj = socket.socket()
        try:
            socket_obj.connect((host, port))
        except Exception as err:
            print err.message

        while True:
            read, write, execute = select.select(
                [socket_obj, channel], [], [])

            if socket_obj in read:
                data = socket_obj.recv(1024)
                if len(data) == 0:
                    break
                print data
                channel.send(data)

            if channel in read:
                data = channel.recv(1024)
                print data
                if len(data) == 0:
                    break
                print data
                socket_obj.send(data)
        channel.close()
        socket_obj.close()

    def get_host_port(self, host_param, default_port):
        """Parse host parameter with optional port number.

        :param host_param: hostname param with/without port (type str)
        :param default_port: default port when port ommited (type int)
        :return parsed_host_params : parsed host parameters (type tuple)
        """
        try:
            params = (host_param.split(":", 1) + [default_port])[:2]
            params[1] = int(params(1))
            parsed_host_params = (params[0],
                                  params[1])
            return parsed_host_params

        except Exception as err:
            print err.message
            return None

    def reverse_forward_tunnel(self,
                               server_port,
                               remote_host,
                               remote_port,
                               transport):
        r"""reverse_forward_tunnel method.

        :param server_port: target server port (type int)
        :param remote_host: relay server address (type str)
        :param remote_port: relay server reverse port (type int)
        :param transport: relay server connection transport \
        (type paramiko.transport.Transport)
        """
        transport.request_port_forward('', server_port)

        while True:
            channel = transport.accept(1000)
            if channel is None:
                continue
            socket_handler_thread = threading.Thread(
                target=ShellTunnelForwarder.reverse_socket_handler,
                args=(channel, remote_host, remote_port))
            socket_handler_thread.setDaemon(True)
            socket_handler_thread.start()
