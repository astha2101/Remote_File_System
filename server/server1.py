import socket
import threading
import sys
import os
class Processor(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock=sock
        self.start()
    def run(self):
        data_bytes=b''
        to_receive=100
#length of request string
        while len(data_bytes)<to_receive:
            by=self.sock.recv(to_receive-len(data_bytes))
            data_bytes+=by
        request_string_length=int(data_bytes.decode("utf-8").strip())
        print("Length of request received as ",request_string_length)
        ack="12"
        self.sock.sendall(bytes(ack,"utf-8"))
#receiving request string
        data_bytes=b''
        to_receive=request_string_length
        while len(data_bytes)<to_receive:
            by=self.sock.recv(to_receive-len(data_bytes))
            data_bytes+=by
        request=data_bytes.decode("utf-8")
        print("Request received as ",request)
        ack="12"
        self.sock.sendall(bytes(ack,"utf-8"))
        if request=="shutdown":
            os._exit(0)
            sys.exit()
        files=os.listdir('c:\pyeg\proj1\server\store')
# sending number of files
        self.sock.sendall(bytes(str(len(files)).ljust(100),"utf-8"))
# sending files name        
        for i in files:
            self.sock.sendall(bytes(str(len(i)).ljust(100),"utf-8"))
            file_name=str(i);           
            self.sock.sendall(bytes(file_name,"utf-8"))
            data_bytes=b''
            to_receive=2
            while len(data_bytes)<to_receive:
                by=self.sock.recv(to_receive-len(data_bytes))
                data_bytes+=by
            ack=data_bytes.decode("utf-8")
# receiving response
        data_bytes=b''
        to_receive=100
        while len(data_bytes)<to_receive:
            by=self.sock.recv(to_receive-len(data_bytes))
            data_bytes+=by
        response_length=int(data_bytes.decode("utf-8").strip())
        to_receive=response_length
        data_bytes=b''
        while len(data_bytes)<to_receive:
            by=self.sock.recv(to_receive-len(data_bytes))
            data_bytes+=by
        response=data_bytes.decode("utf-8")
        print("Response: ",response) 


serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(("localhost",5500))
serverSocket.listen()
while True:
    print("Server is in listening mode")
    sock,socket_name=serverSocket.accept()
    pr=Processor(sock)
