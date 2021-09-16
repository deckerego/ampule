def expected_response(status, body):
    length = len(body)
    header = "HTTP/1.1 " + str(status)
    header += " OK\r\nServer: Ampule/0.0.1-alpha (CircuitPython)\r\nConnection: close\r\n"
    header += "Content-Length: " + str(length)
    header += "\r\n\r\n"
    return header + body + "\r\n"
