import mocket
from unittest import mock
import ampule

HEADER = "HTTP/1.1 %i OK\r\nServer: Ampule/0.0.1-alpha (CircuitPython)\r\nConnection: close\r\n\r\n"

@ampule.route("/param")
def trailing_variable(request):
    return (200, {}, "RESPONSE: %s" % (request.params['myval']))

@ampule.route("/params")
def trailing_variable(request):
    return (200, {}, "RESPONSE: %s %s" % (request.params['myval'], request.params['notmyval']))

def test_query_param():
    socket = mocket.Mocket("GET /param?myval=nothingness HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with((HEADER % 200) + "RESPONSE: nothingness\r\n")
    socket.close.assert_called_once()

def test_query_params():
    socket = mocket.Mocket("GET /params?myval=nothingness&notmyval=brightness HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with((HEADER % 200) + "RESPONSE: nothingness brightness\r\n")
    socket.close.assert_called_once()
