import mocket
from unittest import mock
import ampule
import http_helper

@ampule.route("/var/get", method='GET')
def trailing_variable(request):
    return (200, {}, "GET: %s" % request.body)

def test_body_resend():
    body = "Let me tell you a long rambling story child. Once upon a time there was a coaster on my desk that had a picture of a ship. It was blue. Blue like the ocean? No. Blue like a coaster."
    socket = mocket.Mocket(("GET /var/get HTTP/1.1\r\n\r\n" + body).encode("utf-8"))
    ampule.listen(socket)
    expected = [ # Expect two calls, the second after an 256 byte partial data send
        mock.call(http_helper.expected_response(200, "GET: "+body)),
        mock.call(b"e ocean? No. Blue like a coaster.\r\n")
    ]
    assert socket.send.mock_calls == expected
    socket.close.assert_called_once()
