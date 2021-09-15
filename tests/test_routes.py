import mocket
from unittest import mock
import ampule

HEADER = "HTTP/1.1 %i OK\r\nServer: Ampule/0.0.1-alpha (CircuitPython)\r\nConnection: close\r\n\r\n"

@ampule.route("/default")
def simple_get_route(request):
    return (200, {}, "DEFAULT RESPONSE")

@ampule.route("/get", method='GET')
def simple_get_route(request):
    return (200, {}, "GET RESPONSE")

@ampule.route("/post", method='POST')
def simple_get_route(request):
    return (200, {}, "POST RESPONSE")

@ampule.route("/post", method='GET')
def simple_get_route(request):
    return (400, {}, "WRONG RESPONSE")

def test_miss_default():
    socket = mocket.Mocket("GET /nothing HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with((HEADER % 404) + "Not found\r\n")
    socket.close.assert_called_once()

def test_route_default():
    socket = mocket.Mocket("GET /default HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with((HEADER % 200) + "DEFAULT RESPONSE\r\n")
    socket.close.assert_called_once()

def test_route_get():
    socket = mocket.Mocket("GET /get HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with((HEADER % 200) + "GET RESPONSE\r\n")
    socket.close.assert_called_once()

def test_route_post():
    socket = mocket.Mocket("POST /post HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with((HEADER % 200) + "POST RESPONSE\r\n")
    socket.close.assert_called_once()
