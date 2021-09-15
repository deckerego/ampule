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


## Building ampule

ampule can be added as a .py file into CIRCUITPY projects, or it can be
used as a MicroPython compiled library and added to the `lib/` folder
of a CIRCUITPY project.

### Building MicroPython libraries

After installing the `mpy-cross` compiler from
https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library?view=all#mpy-2982472-11
you can execute:

    mpy-cross ampule.py

To build a MicroPython compiled library.

### Running tests

Tests require pytest to be installed:

    pip3 install -e .
    pytest
