import board
import wifi
import socketpool
import ampule
from digitalio import DigitalInOut, Direction

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "Access-Control-Allow-Origin": '*',
    "Access-Control-Allow-Methods": 'GET, POST',
    "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
}

@ampule.route("/on")
def light_on(request):
    led.value = True
    return (200, headers, '{"enabled": true}')

@ampule.route("/off")
def light_off(request):
    led.value = False
    return (200, headers, '{"enabled": false}')

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
