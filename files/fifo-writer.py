import random
import time
FIFO = 'test.fifo'

new_volume = 50
with open(FIFO,"w") as fp:

    while True:

        fp.write('{}:{}\n'.format(
            random.random(),
            random.random()
        ))
        fp.flush()
        time.sleep(0.1)