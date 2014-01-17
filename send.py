#!/usr/bin/env python
"""Usage:
  send.py [-hv] [--socket SOCKET] [--baud-rate RATE] [--timings-file FILE] ( <section> <command> | <timings> )

Options:
  -h --help               show this help and exit
  -v --version            show version and exit
  -t --timings-file FILE  specify the timings file to use [default: timings.yml]
  -s --socket SOCKET      specify the socket to connect to [default: /dev/ttyACM0]
  -b --baud-rate RATE     the baud rate to connect with [default: 9600]
"""

import serial
import yaml

from docopt import docopt

arguments = docopt(__doc__, version="0.1.0")

if arguments.get("<section>") and arguments.get("<command>"):
    timing_dict = yaml.load(open(arguments["--timings-file"]))
    raw_timings = timing_dict[arguments["<section>"]][arguments["<command>"]]
elif arguments.get("<timings>"):
    raw_timings = arguments["<timings>"]

timings = [int(timing) for timing in raw_timings.split()]
output = "".join([chr(int(round(timing / 25.0))) for timing in timings])

com = serial.Serial(arguments["--socket"], int(arguments["--baud-rate"]), timeout=0.2)
com.write(output + chr(0))
print com.read(1000)
