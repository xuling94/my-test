import socket
from collections import deque

from .udpsocket import *
from .udpsocket import _ERRNO_WOULDBLOCK
from .utils import *

from tornado.ioloop import IOLoop
from tornado.gen import coroutine, Return, Future

class UDPClient(object):
    def __init__(self, server, addr):
        self.addr = addr
        self._inbound_packet = deque(maxlen=500)
        self.shutdown = False
        self._server = server
        self._writeto = server._writeto

        self._waiting_packet = None

    def write(self, data):
        return self._writeto(data, self.addr)

    def has_packet(self):
        return bool(self._inbound_packet)

    def push_packet(self, packet):
        inbound = self._inbound_packet
        b_left = len(inbound) - inbound.maxlen
        if b_left >= 0:
            return # drop packet

        inbound.append(packet)
        if b_left == -1:
            raise BufferFull()

    @coroutine
    def get_next_packet(self):
        assert self._waiting_packet is None
        # Only one coroutine can wait for incoming packet

        if not self._inbound_packet:
            f = FutureExt()
            self._waiting_packet = f
            yield f

        b = self._inbound_packet.popleft()

        raise Return(b)

    def _wake_get_next_packet(self):
        if self._waiting_packet is None:
            return

        if not self._inbound_packet:
            return

        self._waiting_packet.set_result(None)
        self._waiting_packet = None

    def _shutdown_get_next_packet(self):
        if self._waiting_packet is None:
            return

        self._waiting_packet.cancel()
        self._waiting_packet = None

    def closed(self):
        return self.shutdown

    def close(self):
        self._server.on_close(self)
        self._shutdown_get_next_packet()
        del self._server.clients[self.addr]
        self.shutdown = True

