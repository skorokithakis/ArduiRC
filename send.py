#!/usr/bin/env python

import serial
import sys
import time

if len(sys.argv) == 2:
    timings = [int(timing) for timing in sys.argv[1].split()]
else:
    print "Usage:\n\tsend.py <timings>"
    sys.exit(1)

com = serial.Serial("/dev/ttyACM0", 9600, timeout=0.2)

output = "".join([chr(timing / 25) for timing in timings])
com.write(output + chr(0))
print com.read(1000)
