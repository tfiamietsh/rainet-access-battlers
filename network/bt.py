import bluetooth
import socket
from misc import utils
from functools import partial

BUFFER_SIZE = 1024
DEFAULT_PORT = 19


def is_bluetooth_enabled():
    return not isinstance(utils.try_else(get_device_addr), Exception)


def get_device_name():
    return socket.gethostname()


def get_device_addr():
    return bluetooth.read_local_bdaddr()[0]


def discover_devices():
    return utils.try_else(partial(bluetooth.discover_devices, duration=10, lookup_names=True))


class Server:
    def __init__(self):
        self._socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self._socket.bind((get_device_addr(), DEFAULT_PORT))
        self._socket.listen(1)
        self._client_socket = None

    def wait_for_connection(self):
        result = utils.try_else(self._socket.accept)
        if isinstance(result, Exception):
            return result
        else:
            self._client_socket, _ = result

    def send(self, data):
        self._client_socket.send(data)

    def recv(self):
        return self._client_socket.recv(BUFFER_SIZE).decode('utf-8')

    def close(self):
        if self._socket is not None:
            self._socket.close()
        if self._client_socket is not None:
            self._client_socket.close()


class Client:
    def __init__(self):
        self._socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def connect(self, server_addr):
        return utils.try_else(partial(self._socket.connect, addrport=(server_addr, DEFAULT_PORT)))

    def send(self, data):
        self._socket.send(data)

    def recv(self):
        return self._socket.recv(BUFFER_SIZE).decode('utf-8')

    def close(self):
        if self._socket is not None:
            self._socket.close()
