import io

def expected_response(status, body, headers={}):
    header = "HTTP/1.1 " + str(status) + " OK\r\n"
    for k, v in headers.items():
        header += "%s: %s\r\n" % (k, v)
    header += "Server: Ampule/0.0.1-alpha (CircuitPython)\r\nConnection: close\r\n"
    header += "Content-Length: " + str(len(body))
    header += "\r\n\r\n"

    with io.BytesIO() as response:
        response.write(header.encode())

        if isinstance(body, str):
            response.write(body.encode())
        else:
            response.write(body)
        response.write(b"\r\n")

        response.flush()
        response.seek(0)
        return response.read()
