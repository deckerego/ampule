import mocket
from unittest import mock
import ampule

HEADER = "HTTP/1.1 %i OK\r\nServer: Ampule/0.0.1-alpha (CircuitPython)\r\nConnection: close\r\n\r\n"

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
    socket.send.assert_called_once_with((HEADER % 200) + "RESPONSE: gouda\r\n")
    socket.close.assert_called_once()

def test_embedded_var():
    socket = mocket.Mocket("GET /var/quartz/update HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with((HEADER % 200) + "RESPONSE: quartz\r\n")
    socket.close.assert_called_once()

def test_missing_var():
    socket = mocket.Mocket("GET /var/ HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with((HEADER % 404) + "Not found\r\n")
    socket.close.assert_called_once()

def test_double_var():
    socket = mocket.Mocket("GET /var/quartz/gouda HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with((HEADER % 200) + "RESPONSE: gouda quartz\r\n")
    socket.close.assert_called_once()
