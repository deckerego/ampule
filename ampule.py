import io
import re

BUFFER_SIZE = 256
routes = []
variable_re = re.compile("^<([a-zA-Z]+)>$")

class Request:
    def __init__(self, method, full_path):
        self.method = method
        self.path = full_path.split("?")[0]
        self.params = Request.__parse_params(full_path)
        self.headers = {}
        self.body = None

    @staticmethod
    def __parse_params(path):
        query_string = path.split("?")[1] if "?" in path else ""
        param_list = query_string.split("&")
        params = {}
        for param in param_list:
            key_val = param.split("=")
            if len(key_val) == 2:
                params[key_val[0]] = key_val[1]
        return params


def __parse_headers(reader):
    headers = {}
    for line in reader:
        if line == '\r\n': break
        title, content = line.split(":", 1)
        headers[title.strip().lower()] = content.strip()
    return headers

def __parse_body(reader):
    data = ""
    for line in reader:
        if line == '\r\n': break
        data += line
    return data

def __read_request(client):
    try:
        request = ""
        while True:
            client.setblocking(False)
            buffer = bytearray(BUFFER_SIZE)
            client.recv_into(buffer)
            buffer = buffer.replace(b'\x00', b'')
            if len(buffer) <= 0: break
            request += buffer.decode("utf-8")
        reader = io.StringIO(request)
    except OSError:
        return None

    line = reader.readline()
    (method, full_path, version) = line.rstrip("\r\n").split(None, 2)

    request = Request(method, full_path)
    request.headers = __parse_headers(reader)
    request.body = __parse_body(reader)

    return request

def __send_response(client, code, headers, data):
    headers["Server"] = "Ampule/0.0.1-alpha (CircuitPython)"
    headers["Connection"] = "close"
    headers["Content-Length"] = len(data)

    response = "HTTP/1.1 %i OK\r\n" % code
    for k, v in headers.items():
        response += "%s: %s\r\n" % (k, v)
    response += "\r\n" + data + "\r\n"

    client.send(response)

def __on_request(method, rule, request_handler):
    regex = "^"
    rule_parts = rule.split("/")
    for part in rule_parts:
        # Is this portion of the path a variable?
        var = variable_re.match(part)
        if var:
            # If so, allow any alphanumeric value
            regex += r"([a-zA-Z0-9_-]+)\/"
        else:
            # Otherwise exact match
            regex += part + r"\/"
    regex += "?$"
    routes.append(
        (re.compile(regex), {"method": method, "func": request_handler})
    )

def __match_route(path, method):
    for matcher, route in routes:
        match = matcher.match(path)
        if match and method == route["method"]:
            return (match.groups(), route)
    return None

def listen(socket):
    client, remote_address = socket.accept()
    try:
        client.settimeout(30)
        request = __read_request(client)
        if request:
            match = __match_route(request.path, request.method)
            if match:
                args, route = match
                status, headers, body = route["func"](request, *args)
                __send_response(client, status, headers, body)
            else:
                __send_response(client, 404, {}, "Not found")
        else:
            __send_response(client, 204, {}, "")
    except:
        __send_response(client, 500, {}, "Error processing request")
    client.close()

def route(rule, method='GET'):
    return lambda func: __on_request(method, rule, func)
