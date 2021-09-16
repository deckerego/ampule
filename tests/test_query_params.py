import mocket
from unittest import mock
import ampule
import http_helper

@ampule.route("/param")
def trailing_variable(request):
    return (200, {}, "RESPONSE: %s" % (request.params['myval']))

@ampule.route("/params")
def trailing_variable(request):
    return (200, {}, "RESPONSE: %s %s" % (request.params['myval'], request.params['notmyval']))

def test_query_param():
    socket = mocket.Mocket("GET /param?myval=nothingness HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(200, "RESPONSE: nothingness"))
    socket.close.assert_called_once()

def test_query_params():
    socket = mocket.Mocket("GET /params?myval=nothingness&notmyval=brightness HTTP/1.1".encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(200, "RESPONSE: nothingness brightness"))
    socket.close.assert_called_once()
