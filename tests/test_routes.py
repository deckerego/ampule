import mocket
from unittest import mock
import ampule
import http_helper

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
    socket.send.assert_called_once_with(http_helper.expected_response(404, "Not found"))
    socket.close.assert_called_once()

def test_route_default():
    socket = mocket.Mocket("GET /default HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(200, "DEFAULT RESPONSE"))
    socket.close.assert_called_once()

def test_route_get():
    socket = mocket.Mocket("GET /get HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(200, "GET RESPONSE"))
    socket.close.assert_called_once()

def test_route_post():
    socket = mocket.Mocket("POST /post HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(200, "POST RESPONSE"))
    socket.close.assert_called_once()
