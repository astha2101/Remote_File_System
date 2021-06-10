import socket
import os
import sys
socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect(("localhost",5500))
request="Dir";
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
#receiving number of files
data_bytes=b''
to_receive=100
while len(data_bytes)<to_receive:
   by=socket.recv(to_receive-len(data_bytes))
   data_bytes+=by
number_of_files=int(data_bytes.decode("utf-8").strip())
print("Number of files received as",number_of_files)
files=[]
for i in range(number_of_files):
    data_bytes=b''
    to_receive=100
    while len(data_bytes)<to_receive:
       by=socket.recv(to_receive-len(data_bytes))
       data_bytes+=by
    length_of_file_name=int(data_bytes.decode("utf-8").strip())
    data_bytes=b''
    to_receive=length_of_file_name
    while len(data_bytes)<to_receive:
       by=socket.recv(to_receive-len(data_bytes))
       data_bytes+=by
    file_name=data_bytes.decode("utf-8")
    files.append(file_name)
    ack="12"
    socket.sendall(bytes(ack,"utf-8"))
response="All files received !!"
socket.sendall(bytes(str(len(response)).ljust(100),"utf-8"))
socket.sendall(bytes(response,"utf-8"))
for i in files:
    print(i)
socket.close()
    