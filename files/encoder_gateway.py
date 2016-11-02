#!/usr/bin/env python

import argparse
import os
import socket
import sys
from thread import start_new_thread

DEFAULT_HOST = ''
DEFAULT_PORT = 8888

level_data = {
    'level_avg': 0.0,
    'level': 0.0,
    'levels': [0 for x in range(0,100)]
}

class Gateway(object):

    def __init__(self, opts):
        self.opts = opts

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((DEFAULT_HOST, self.opts.port))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        self.socket.listen(10)

    def run(self):

        start_new_thread(self.thread_fifo, (None,))
        while 1:
            connection, addr = self.socket.accept()
            start_new_thread(self.thread_socket, (connection,))

        self.socket.close()



    def thread_fifo(self, cb):

        f = open(self.opts.fifo, 'r')

        while True:
            for line in iter(f.readline, ''):
                line = line.strip()

                level_left, level_right = line.split(':')
                level = (float(level_left) + float(level_right)) * 0.5

                level_data['levels'].insert(0, level)
                level_data['levels'].pop()

                level_data['level'] = level
                level_data['level_avg'] = reduce(lambda x, y: x + y, level_data['levels']) / len(level_data['levels'])


    def thread_socket(self, connection):

        while True:

            key = connection.recv(1024)
            key = key.replace('\n', '')

            if not key:
                break

            try:
                reply = '{}'.format(level_data[key])
            except:
                reply = 'invalid key'

            connection.sendall(reply)

        connection.close()




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'encoder gateway')

    parser.add_argument('-f', '--fifo', dest='fifo', required=True)
    parser.add_argument('-p', '--port', dest='port', default=DEFAULT_PORT)

    opts = parser.parse_args()

    g = Gateway(opts=opts)
    g.run()
