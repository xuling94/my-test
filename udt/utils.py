import os
import errno
import struct
import socket
from collections import deque
from traceback import extract_stack

from tornado.ioloop import IOLoop
from tornado.gen import coroutine, Return, Future


def _set_stack(exc):
    exc.__traceback__ = extract_stack()
    return exc

class BufferFull(Exception):
    pass

class Shutdown(Exception):
    pass

class Cancel(Exception):
    pass

class FutureExt(Future):

    def cancel(self):
        self.set_exception(Cancel())

    def cancelled(self):
        return isinstance(self.exception(), Cancel)
