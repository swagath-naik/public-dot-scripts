#!/usr/bin/env python3
import socket
import sys
import argparse
import os
import json

parser = argparse.ArgumentParser(description='Send Files to Socket Receiver')
parser.add_argument('ip', type=str, help='ip address of receiver')
parser.add_argument('port', type=int, help='port no of receiver')
parser.add_argument('file', type=str, help='filename to send')
args = parser.parse_args()
print(args.ip,args.port,args.file)


s = socket.socket()

#IP = socket.gethostname()
IP = args.ip
PORT = args.port

s.connect((IP, PORT))

#file_name = 'R Programming Tutorial-s3FozVfd7q4.mkv'
file_name = args.file
file = open(file_name, "rb")
file_size = os.path.getsize(file_name)
data = { 'file_name' : os.path.basename(file_name), 'file_size' : file_size}
SendData = json.dumps(data).encode()


while SendData:
    s.send(SendData)
    SendData = file.read(1024)
s.close()

