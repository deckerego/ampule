import mocket
from unittest import mock
import ampule
import http_helper

def test_socket_error():
    socket = mocket.Mocket("GET /bad HTTP/1.1".encode("utf-8"))
    socket.settimeout = mock.Mock(side_effect=OSError('SetTimeout'))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(500, "Error processing request"))
    socket.close.assert_called_once()

def test_empty_request():
    socket = mocket.Mocket("GET /bad HTTP/1.1".encode("utf-8"))
    socket.recv_into = mock.Mock(side_effect=OSError('ReceiveInto'))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(204, ""))
    socket.close.assert_called_once()
