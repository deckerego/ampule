# ampule

A tiny HTTP server made for CircuitPython WiFi devices (like the ESP32).

Note that ampule is in alpha and right now for use by
[tally_circuitpy](https://github.com/deckerego/tally_circuitpy). Feel free to
use it, but know that there are tons of things not yet implemented.

ampule gathers inspiration from
[Bottle: Python Web Framework](https://bottlepy.org/docs/dev/index.html),
Adafruit's [CircuitPython WSGI](https://github.com/adafruit/Adafruit_CircuitPython_WSGI)
library, Adafruit's [ESP32 SPI WSGI Server](https://github.com/adafruit/Adafruit_CircuitPython_ESP32SPI/blob/main/adafruit_esp32spi/adafruit_esp32spi_wsgiserver.py),
and Adafruit's [CircuitPython Requests library](https://github.com/adafruit/Adafruit_CircuitPython_Requests).

## Usage

Route definitions in ampule are expressed through annotations that define the
path and optionally the method to be matched against for incoming HTTP requests.
ampule will pass along the request and any path elements that operate as arguments,
and expects the HTTP status code, headers, and body to be returned as a tuple.

### "Hello World" Example

The following example is a simple, working HTTP server that accepts an
HTTP GET request at `/hello` and responds with "Hi There!".

```python
import ampule, socketpool, wifi

@ampule.route("/hello")
def hello(request):
    return (200, {}, 'Hi There!')

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets not found in secrets.py")
    raise

try:
    print("Connecting to {}...".format(secrets["ssid"]))
    wifi.radio.connect(secrets["ssid"], secrets["password"])
except:
    print("Error connecting to WiFi")
    raise

pool = socketpool.SocketPool(wifi.radio)
socket = pool.socket()
socket.bind(['0.0.0.0', 80])
socket.listen(1)
print("Connected to {}, Web server running on http://{}:80".format(secrets["ssid"], wifi.radio.ipv4_address))

while True:
    ampule.listen(socket)
```

The majority of this code is CircuitPython boilerplate that connects to a WiFi
network, listens on port 80, and connects ampule to the open socket.

The line `@ampule.route("/hello")` registers the following function for
the path specified, and responds with HTTP 200, no headers, and a response body
of "Hi There!"

### Variables in the URL Path

Route paths can also contain variables, as in:

```python
@ampule.route("/hello/<name>")
def hello(request, name):
    return (200, {}, "Hi there {}!".format(name))
```

### Query Parameters

Query parameters are passed along with the request. If a URL ends with
`/hello?name=Bob` then the following route will return
"Hi there Bob!":

```python
@ampule.route("/hello")
def hello(request):
    name = request.params["name"]
    return (200, {}, "Hi there {}!".format(name))
```

### Specifying HTTP Method on Routes

You can explicitly specify the HTTP method on a route. If it is omitted,
the match defaults to 'GET'.

```python
@ampule.route("/hello", method='POST')
def hello(request):
    name = request.params["name"]
    return (200, {}, "Hi there {}!".format(name))
```

### Specifying Headers

Headers are returned as part of the returned tuple in the route handler.
As an example, returning JSON content and permitting cross-origin access
would be:

```python
headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "Access-Control-Allow-Origin": '*',
    "Access-Control-Allow-Methods": 'GET, POST',
    "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
}

@ampule.route("/hello")
def hello(request):
    return (200, headers, '{"hello": true}')
```

## Building ampule

ampule can be added as a .py file into CIRCUITPY projects, or it can be
used as a MicroPython compiled library and added to the `lib/` folder
of a CIRCUITPY project.

### Building MicroPython libraries

After installing the `mpy-cross` compiler from
https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library?view=all#mpy-2982472-11
you can execute:

```sh
mpy-cross ampule.py
```

To build a MicroPython compiled library.

### Running tests

Tests require `pytest` to be installed along with a local version of ampule, as in:

```sh
pip3 install -e .
```

Once installed pytest can be invoked with default arguments, as in:

```sh
pytest
```
