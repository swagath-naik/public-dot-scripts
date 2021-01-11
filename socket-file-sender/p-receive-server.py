import socket
import sys
import argparse
import json
import netifaces

def print_line(no_of_lines=24):
	print('-'*no_of_lines)

parser = argparse.ArgumentParser(description='Socket Receive Server')
parser.add_argument('port', type=int, help='port number')
args = parser.parse_args()
#print(args.port)


s = socket.socket()
PORT = args.port
s.bind(('', PORT))
#ip_addrs=[i[4][0] for i in socket.getaddrinfo(socket.gethostname(), PORT)]
ip_addrs=[]
for iface in netifaces.interfaces():
    iface_details = netifaces.ifaddresses(iface)
    if netifaces.AF_INET in iface_details:
        # print(iface_details[netifaces.AF_INET])
        for ip_interfaces in iface_details[netifaces.AF_INET]:
            for key, ip_add in ip_interfaces.items():
                if key == 'addr' and ip_add != '127.0.0.1':
                    ip_addrs.append(ip_add)
print_line()
print("Receiver Server IP:")
for i in ip_addrs:
	print(i)
print_line()
print("Port :", PORT)
print_line()

s.listen(10)


while True:
    try:
        conn, addr = s.accept()
    except KeyboardInterrupt:
        print()
        exit(0)
    RecvData = conn.recv(2048)
    
    f_info=json.loads(RecvData)
    print(f_info)
    
    file = open('Recv-'+f_info['file_name'],'wb')
    RecvData = conn.recv(1024)
    
    while RecvData:
        file.write(RecvData)
        RecvData = conn.recv(1024)
    file.close()
    
    print(f"File {'Recv-'+f_info['file_name']} received.")
    conn.close()
    # print("Server closed the connection \n")
    print_line()
