ArduiRC
=======

Remotely control IR/RF devices from a computer with Arduino.

Rationale
---------
The reason for this library is explained in [a post I wrote about it](http://www.stavros.io/posts/control-rf-devices-with-arduino/). Basically, I needed my home server to be able to control RF devices, and here we are.

Usage
-----
To use ArduiRC, you need to perform two steps:

1. Install the Arduino sketch on the device so it can transmit the codes (after you've set up the Arduino with the proper hardware).
2. Use `arduirc.py` to transfer the code you want to transmit to the Arduino for transmission.

To install the sketch to the Arduino, either use the IDE to compile and upload `sketch.ino`, or use the amazing [Ino](http://inotool.org/):

    ino build
    ino upload

Afterwards, use `arduirc.py` to send the timings (which you can retrieve by reading the post above):

    ./arduirc.py "625 625 1292 646 1292 625 1292 646 1271 667 1271 646 1271 646"

You can also define the timings in a YAML file so you don't have to enter the numbers each time:

    ./arduirc.py garage open

The `timings.yml` file for the above command might look something like this:

    garage:
      open: 625 625 1292 646 1292 625 1292 646 1271 667 1271 646 1271 646
      close: 625 625 1292 625 625 1292 646 1292 625 1292 625 1292 667 1271 646
    ac:
      toggle: 625 625 1292 646 1292 625 1292 625 1292 667 1271 646 127

Hopefully this will be enough to get you started.
