import socket


def check_port(address, port):
    """Check if port is open or not.

    :param address: ipv4 addres of target machine (type str)
    :param port: port of target machine (type int)
    :return result: True/False based on port availability (type boolean)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((address, port))
        if result == 0:
            result = False
        else:
            result = True
        return result

    except Exception as err:
        print err.message
