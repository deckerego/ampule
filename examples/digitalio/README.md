# Digital I/O Example

This example allows the board's LED to be remotely controled using
basic REST commands.

## Examples

Turn on the LED:

```sh
curl -v http://192.168.0.1:7413/on
```

Turning it off again:

```sh
curl -v http://192.168.0.1:7413/off
```
