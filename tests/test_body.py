import mocket
from unittest import mock
import ampule

HEADER = "HTTP/1.1 %i OK\r\nServer: Ampule/0.0.1-alpha (CircuitPython)\r\nConnection: close\r\n\r\n"

@ampule.route("/var/get")
def trailing_variable(request):
    return (200, {}, "RESPONSE: %s" % request.body)

def test_body_get():
    body = "Howdy there"
    socket = mocket.Mocket(("GET /var/get HTTP/1.1\r\n\r\n" + body).encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with((HEADER % 200) + "RESPONSE: Howdy there\r\n")
    socket.close.assert_called_once()
