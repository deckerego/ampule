import mocket
from unittest import mock
import ampule

HEADER = "HTTP/1.1 %i OK\r\nServer: Ampule/0.0.1-alpha (CircuitPython)\r\nConnection: close\r\n\r\n"

def test_socket_error():
    socket = mocket.Mocket("GET /bad HTTP/1.1".encode("utf-8"))
    socket.settimeout = mock.Mock(side_effect=OSError('SetTimeout'))
    ampule.listen(socket)
    socket.send.assert_called_once_with((HEADER % 500) + "Error processing request\r\n")
    socket.close.assert_called_once()

def test_empty_request():
    socket = mocket.Mocket("GET /bad HTTP/1.1".encode("utf-8"))
    socket.recv_into = mock.Mock(side_effect=OSError('ReceiveInto'))
    ampule.listen(socket)
    socket.send.assert_called_once_with((HEADER % 204) + "\r\n")
    socket.close.assert_called_once()
