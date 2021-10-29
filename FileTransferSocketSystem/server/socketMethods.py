import sys
import socket
import os

def send_file(socket, filename) :
    with open(filename, "rb") as f:
        data = f.read()

    bytes_sent = socket.sendall(data)
    return bytes_sent

def recv_file(socket, filename):
    data = bytearray(1)
    bytes_read = 0

    with open(filename, 'wb') as f:
        while data:

            data = socket.recv(1024)
            bytes_read += len(data)

            f.write(data)

    return bytes_read

def send_listing(socket):
    path = "C:/Users/kalfo/Documents/University2/NOSE2/Assessed-exercise-1/server"
    dirs = os.listdir(path)

    dirs = " ".join(dirs)
    bytes_sent = socket.sendall(str.encode(dirs))

    return bytes_sent


def recv_listing(socket):
    data = bytearray(1)
    bytes_read = 0
    array_str = ""

    while data:
        data = socket.recv(1024)
        bytes_read += len(data)

        array_str += data.decode()

    array = array_str.split(' ')
    for elt in array:
        print(elt)

    return bytes_read