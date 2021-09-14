# SPDX-License-Identifier: Unlicense
#
# SPDX-ExternalRefComment: Inspired By Adafruit's CircuitPython Requests test package
# SPDX-ExternalRef: OTHER https://github.com/adafruit/Adafruit_CircuitPython_Requests/blob/74b0a5a0590923aec6bc17c8783ae9b35b234aad/tests/mocket.py

""" Mock Socket """

from unittest import mock


class MocketPool:
    """ Mock SocketPool """

    SOCK_STREAM = 0

    def __init__(self):
        self.getaddrinfo = mock.Mock()
        self.socket = mock.Mock()


class Mocket:
    """ Mock Socket """

    def __init__(self, request):
        self.settimeout = mock.Mock()
        self.setblocking = mock.Mock()
        self.close = mock.Mock()
        self.connect = mock.Mock()
        self.accept = mock.Mock(side_effect=self._accept)
        self.send = mock.Mock(side_effect=self._send)
        self.recv = mock.Mock(side_effect=self._recv)
        self.recv_into = mock.Mock(side_effect=self._recv_into)
        self._position = 0
        self._response = request

    def _accept(self):
        return (self, ('0.0.0.0', 0))

    def _send(self, data):
        return len(data)

    def _recv(self, count):
        end = self._position + count
        response = self._response[self._position : end]
        self._position = end
        return response

    def _recv_into(self, buf, nbytes=0):
        assert isinstance(nbytes, int) and nbytes >= 0
        read = nbytes if nbytes > 0 else len(buf)
        remaining = len(self._response) - self._position
        if read > remaining:
            read = remaining
        end = self._position + read
        buf[:read] = self._response[self._position : end]
        self._position = end
        return
