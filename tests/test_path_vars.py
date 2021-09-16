import mocket
from unittest import mock
import ampule
import http_helper

@ampule.route("/var/<cheeses>")
def trailing_variable(request, cheeses):
    return (200, {}, "RESPONSE: %s" % cheeses)

@ampule.route("/var/<rocks>/update")
def embedded_variable(request, rocks):
    return (200, {}, "RESPONSE: %s" % rocks)

@ampule.route("/var/<rocks>/<cheeses>")
def embedded_variable(request, rocks, cheeses):
    return (200, {}, "RESPONSE: %s %s" % (cheeses, rocks))

def test_trailing_var():
    socket = mocket.Mocket("GET /var/gouda HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(200, "RESPONSE: gouda"))
    socket.close.assert_called_once()

def test_embedded_var():
    socket = mocket.Mocket("GET /var/quartz/update HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(200, "RESPONSE: quartz"))
    socket.close.assert_called_once()

def test_missing_var():
    socket = mocket.Mocket("GET /var/ HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(404, "Not found"))
    socket.close.assert_called_once()

def test_double_var():
    socket = mocket.Mocket("GET /var/quartz/gouda HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(200, "RESPONSE: gouda quartz"))
    socket.close.assert_called_once()
