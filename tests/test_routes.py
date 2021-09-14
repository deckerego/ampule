import pytest
import json
import mocket
import ampule

IP = "1.2.3.4"
HOST = "httpbin.org"
RESPONSE = { }
ENCODED = json.dumps(RESPONSE).encode("utf-8")
HEADERS = (
    (
        "HTTP/1.0 200 OK\r\n\r\n"
        "Content-Type: application/json\r\nContent-Length: {}\r\n\r\n"
    )
    .format(len(ENCODED))
    .encode("utf-8")
)

@ampule.route("/test/get")
def simple_get_route(request):
    return (200, {}, "GET RESPONSE")

def test_url_get():
    socket = mocket.Mocket(HEADERS + ENCODED)
    ampule.listen(socket)
