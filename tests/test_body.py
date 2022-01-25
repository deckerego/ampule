import mocket
from unittest import mock
import ampule
import http_helper

@ampule.route("/var/get", method='GET')
def trailing_variable(request):
    return (200, {}, "GET: %s" % request.body)

@ampule.route("/var/get", method='POST')
def trailing_variable(request):
    return (200, {}, "POST: %s" % request.body)

@ampule.route("/var/download")
def image_download(request):
    return (200, {"Content-Type": "application/octet-stream"}, b"12354")

def test_body_get():
    body = "Howdy there"
    socket = mocket.Mocket(("GET /var/get HTTP/1.1\r\n\r\n" + body).encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(200, "GET: Howdy there"))
    socket.close.assert_called_once()

def test_body_post():
    body = "Howdy there"
    socket = mocket.Mocket(("POST /var/get HTTP/1.1\r\n\r\n" + body).encode("utf-8"))
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(200, "POST: Howdy there"))
    socket.close.assert_called_once()

def test_body_mime():
    expected_bytes = bytearray([0x31,0x32,0x33,0x35,0x34])
    expected_header = {"Content-Type": "application/octet-stream"}
    socket = mocket.Mocket(("GET /var/download HTTP/1.1\r\n\r\n").encode())
    ampule.listen(socket)
    socket.send.assert_called_once_with(http_helper.expected_response(200, expected_bytes, expected_header))
    socket.close.assert_called_once()

def test_body_resend():
    body = "Let me tell you a long rambling story child. Once upon a time there was a coaster on my desk that had a picture of a ship. It was blue. Blue like the ocean? No. Blue like a coaster."
    socket = mocket.Mocket(("GET /var/get HTTP/1.1\r\n\r\n" + body).encode("utf-8"))
    ampule.listen(socket)
    expected = [mock.call(http_helper.expected_response(200, "GET: "+body)), mock.call(b"e ocean? No. Blue like a coaster.\r\n")]
    assert socket.send.mock_calls == expected
    socket.close.assert_called_once()
