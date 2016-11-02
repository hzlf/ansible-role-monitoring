'''
    Simple socket server using threads
'''
import os
import socket
import sys
from thread import *
import random

import time

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

FIFO = 'test.fifo'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'


level_data = {
    'level_avg': 0.0,
    'level': 0.0,
    'levels': [0 for x in range(0,100)]
}

def datathread(bla):

    f = open(FIFO, 'r')

    while True:
        for line in iter(f.readline, ''):
            line = line.strip()

            level_left, level_right = line.split(':')
            level = (float(level_left) + float(level_right)) * 0.5

            level_data['levels'].insert(0, level)
            level_data['levels'].pop()

            level_data['level'] = level
            level_data['level_avg'] = reduce(lambda x, y: x + y, level_data['levels']) / len(level_data['levels'])
            print level_data['level'],
            print level_data['level_avg']




#Function for handling connections. This will be used to create threads
def clientthread(conn):

    while True:

        #Receiving from client
        key = conn.recv(1024)
        key = key.replace('\n', '')

        if not key:
            break

        print 'key:', key

        try:
            reply = '{}'.format(level_data[key])
        except:
            reply = 'invalid key'

        conn.sendall(reply)
        #conn.close()

    #came out of loop
    conn.close()

#now keep talking with the client
start_new_thread(datathread, (None,))
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))


s.close()