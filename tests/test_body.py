import mocket
from unittest import mock
import ampule
import http_helper

@ampule.route("/var/get", method='GET')
def trailing_variable(request):
    return (200, {}, "RESPONSE: %s" % request.body)

@ampule.route("/var/get", method='POST')
def trailing_variable(request):
    return (200, {}, "RESPONSE: %s" % request.body)

def test_body_get():
    body = "Howdy there"
    socket = mocket.Mocket(("GET /var/get HTTP/1.1\r\n\r\n" + body).encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(200, "RESPONSE: Howdy there"))
    socket.close.assert_called_once()

def test_body_post():
    body = "Howdy there"
    socket = mocket.Mocket(("POST /var/get HTTP/1.1\r\n\r\n" + body).encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(200, "RESPONSE: Howdy there"))
    socket.close.assert_called_once()
