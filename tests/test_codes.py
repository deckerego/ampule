import mocket
from unittest import mock, TestCase
import ampule
import errno
import http_helper

class MyTestCase(TestCase):
    def test_socket_error(self):
        socket = mocket.Mocket("GET /bad HTTP/1.1".encode("utf-8"))
        socket.accept = mock.Mock(side_effect=OSError('socket failure'))
        with self.assertRaises(OSError):
            ampule.listen(socket)
        socket.send.assert_not_called()
        socket.close.assert_not_called()

    def test_connection_reset(self):
        socket = mocket.Mocket("GET /bad HTTP/1.1".encode("utf-8"))
        socket.accept = mock.Mock(side_effect=OSError(errno.ECONNRESET))
        socket.send.assert_not_called()
        socket.close.assert_not_called()

    def test_no_data_currently(self):
        socket = mocket.Mocket("GET /bad HTTP/1.1".encode("utf-8"))
        socket.accept = mock.Mock(side_effect=OSError(errno.EAGAIN))
        socket.send.assert_not_called()
        socket.close.assert_not_called()

    def test_routing_error(self):
        socket = mocket.Mocket("GET /bad HTTP/1.1".encode("utf-8"))
        socket.recv_into = mock.Mock(side_effect=OSError('read failure'))
        ampule.listen(socket)
        socket.send.assert_called_once_with(http_helper.expected_response(500, "Error processing request"))
        socket.close.assert_called_once()