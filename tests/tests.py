import socket
import set_src_package
set_src_package.set_src()
from components.common_utils import commons


class TestCommons:
    """Unit Tests for commons module."""

    def test_check_port(self):
        """Unit test for commons.check_port."""
        try:
            target_server = "localhost"
            target_port = 1234
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((target_server, target_port))
            server_sock.listen(10)

            assert not commons.check_port(target_server, target_port)
            server_sock.close()

        except Exception as err:
            print err.message
