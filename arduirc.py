#!/usr/bin/env python
"""Usage:
  arduirc.py [options] ( <section> <command> | <timings> )

Options:
  -h --help               show this help and exit
  -v --version            show version and exit
  -t --timings-file=FILE  specify the timings file to use [default: timings.yml]
  -s --socket=SOCKET      specify the socket to connect to [default: /dev/ttyACM0]
  -w --wait               wait two seconds for the Arduino to reset.
  -b --baud-rate=RATE     the baud rate to connect with [default: 9600]
  -r --repeat=REPEAT      repeat the command REPEAT times [default: 3]
  -d --delay=DELAY        delay between repeats (in usec) [default: 10000]
  -p --pin=PIN            which Arduino pin to write to [default: 3]
"""

import serial
import sys
import time
import yaml

from docopt import docopt


def main(arguments):
    if arguments.get("<section>") and arguments.get("<command>"):
        section = arguments["<section>"]
        command = arguments["<command>"]

        try:
            timing_dict = yaml.load(open(arguments["--timings-file"]))
        except IOError:
            sys.exit("Error opening timings file.")

        if section not in timing_dict:
            sys.exit("Unknown section.")

        if command not in timing_dict[section]:
            sys.exit("Unknown command.")

        raw_timings = timing_dict[section][command]
    elif arguments.get("<timings>"):
        raw_timings = arguments["<timings>"]

    timings = [int(timing) for timing in raw_timings.split()]
    output = "".join([chr(int(round(timing / 25.0))) for timing in timings])

    com = serial.Serial(arguments["--socket"], int(arguments["--baud-rate"]), timeout=0.2)

    if arguments["--wait"]:
        print "Waiting for the Arduino to reset..."
        time.sleep(2)

    pin = int(arguments["--pin"])
    repeat = int(arguments["--repeat"])
    delay = int(round(int(arguments["--delay"]) / 100.0))

    if delay > 255 or delay < 1:
        sys.exit("Delay must be between 100 and 25500.")

    if pin > 13 or pin < 0:
        sys.exit("Pin must be between 0 and 13.")

    if repeat > 255 or repeat < 1:
        sys.exit("Repeat must be between 1 and 255.")

    # chr(1) is the command (command 1, send timings).
    com.write(chr(1) + chr(pin) + chr(repeat) + chr(delay) + output + chr(0))
    print com.read(1000)

if __name__ == "__main__":
    arguments = docopt(__doc__, version="0.1.0")
    main(arguments)
