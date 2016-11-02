#!/usr/bin/env python

import sys
import os
import time

FIFO = '/home/odr/encoder/level.fifo'
fd = os.open(FIFO, os.O_RDONLY)
while True:
    data = os.read(fd, 100)
    if not data:
        time.sleep(0.1)
    else:
        level = data.split("\n")[1]

        level_avg = level.split(',')[0].split(':')[0]

        sys.stdout.write(level_avg)
        sys.exit()
