import os
import sys
import select
import socket
import getpass
import threading
from optparse import OptionParser

import paramiko


class ShellTunnelForwarder:

    def __init__(self):
        self.SSH_PORT = 22
        self.DEFAULT_RELAY_SERVER_PORT = 1234
        self.PKEY_PASSPHRASE = None

        self.verbose_mode = True

    def verbose(self, message):

        if self.verbose_mode:
            print(message)

    def reverse_forward_tunnel(self,
                               server_port,
                               remote_host,
                               remote_port,
                               transport):
        try:
            transport.request_port_forward('', server_port)
            while True:
                channel = transport.accept(1000)
                if channel is None:
                    continue
                #thread_instance = threading.Thread(target=)
        except Exception as err:
            print(err.message)
