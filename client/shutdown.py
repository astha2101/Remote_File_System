import socket
import os
import sys
socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect(("localhost",5500))
request='("shutdown",0)';
#sending length of request
socket.sendall(bytes(str(len(request)).ljust(100),"utf-8"))
print("Length of file request sent.")
data_bytes=b''
to_receive=2
while len(data_bytes)<to_receive:
   by=socket.recv(to_receive-len(data_bytes))
   data_bytes+=by
ack=data_bytes.decode("utf-8")
#sending request 
socket.sendall(bytes(request,"utf-8"))
print("Request sent.")
data_bytes=b''
to_receive=2
while len(data_bytes)<to_receive:
   by=socket.recv(to_receive-len(data_bytes))
   data_bytes+=by
ack=data_bytes.decode("utf-8").strip()


    