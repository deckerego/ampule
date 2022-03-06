import ampule
import socketpool
import wifi
import json
import os

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

# Collect details about the system 
details = {
    "machine": os.uname().machine,
    "release": os.uname().release,
    "platform": os.uname().sysname,
}

def web_page():
    """Content for the web page."""
    content = f"""
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>CircuitPython</title>
        <!-- CSS could also be loaded from local storage or be embedded. --->
        <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/water.css@2/out/water.css'>
    </head>
    <body>
        <h1>CircuitPython</h1>
        <p>This simple web page show some details about your board.</p>
        <!-- All details are shown in a table --->
        <div id="details"></div>     
        <p style='text-align:center;'>Content served by <a href='https://github.com/deckerego/ampule'>ampule</a> and styled with <a href='https://watercss.kognise.dev/'>Water.css</a>.</p>
        <!-- If you include Javascript then keep an eye on the escaping, here it's a Python f-string. --->
        <script>
        window.addEventListener('load', () => {{
            // The dict can not be used directly
            data = JSON.parse('{json.dumps(details)}');

            var table = document.createElement('table'), row, cell1, cell2;
            document.getElementById('details').appendChild(table);
            for (let key in data) {{
              row = table.insertRow();
              cell1 = row.insertCell();
              cell2 = row.insertCell();
              cell1.innerHTML = key;
              cell2.innerHTML = data[key];
            }}
        }});
        </script>
    </body>
    </html>
    """
    return content


def static_file():
    """Load the web page from the CIRCUITPY drive."""
    with open('demo.html') as local_file:
        content = local_file.read()
    return content


@ampule.route("/")
def index(request):
    """Route for the default."""
    return (200, {}, web_page())


@ampule.route("/demo")
def demo(request):
    """Route for the local file."""
    return (200, {}, static_file())


pool = socketpool.SocketPool(wifi.radio)
socket = pool.socket()
socket.bind(['0.0.0.0', 80])
socket.listen(1)
print("Connected to {}, Web server running on http://{}:80".format(secrets["ssid"], wifi.radio.ipv4_address))

while True:
    ampule.listen(socket)
