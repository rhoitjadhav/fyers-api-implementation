# Packages
import zmq
import logging

logger = logging.getLogger(__name__)


class ZMQPublisher:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._context = None
        self._socket = None

    def connect(self):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self._socket.bind(f"tcp://{self._host}:{self._port}")
        logger.info(f"------- ZMQ Publisher Connected at {self._host}:{self._port} -------")

    def send_msg(self, msg):
        if self._socket:
            self._socket.send_string(msg)
        else:
            logger.error("Publisher not connected, try to connect first!")


class ZMQSubscriber:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._context = None
        self._socket = None

    def connect(self):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.SUB)
        self._socket.connect(f"tcp://{self._host}:{self._port}")
        self._socket.setsockopt_string(zmq.SUBSCRIBE, "")

        print(f"------- ZMQ Subscriber Connected at {self._host}:{self._port} -------")

    def get_socket(self):
        if self._socket:
            return self._socket

        logger.error("Subscriber not connected, try to connect first!")
