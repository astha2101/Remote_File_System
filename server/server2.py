import socket
import threading
import sys
import os
class Processor(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock=sock
        self._files=os.listdir('c:\pyeg\proj1\server\store')
        self._files_data=dict()
        for i in self._files:
            file="\\store\\"+i
            path=os.getcwd()+file
            self._files_data[i]=os.path.getsize(path)
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
        if request.lower()=="dir":
            # sending number of files
            self.sock.sendall(bytes(str(len(self._files)).ljust(100),"utf-8"))
            # sending files name        
            for i in self._files:
                self.sock.sendall(bytes(str(len(i)).ljust(100),"utf-8"))           
                self.sock.sendall(bytes(i,"utf-8"))
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
        if request.lower()=="find":
            #length of file name
            data_bytes=b''
            to_receive=100
            while len(data_bytes)<to_receive:
                by=self.sock.recv(to_receive-len(data_bytes))
                data_bytes+=by
            file_name_length=int(data_bytes.decode("utf-8").strip())
            to_receive=file_name_length
            data_bytes=b''
            while len(data_bytes)<to_receive:
                by=self.sock.recv(to_receive-len(data_bytes))
                data_bytes+=by
            file_name=data_bytes.decode("utf-8")
            print("File name: ",file_name)
            if file_name not in self._files_data:
                response="INVALID"
                self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8")) 
                self.sock.sendall(bytes(response,"utf-8"))
                return
            response="VALID" 
            self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8")) 
            self.sock.sendall(bytes(response,"utf-8"))
        if request.lower()=="get":
            #length of file name
            data_bytes=b''
            to_receive=100
            while len(data_bytes)<to_receive:
                by=self.sock.recv(to_receive-len(data_bytes))
                data_bytes+=by
            file_name_length=int(data_bytes.decode("utf-8").strip())
            to_receive=file_name_length
            data_bytes=b''
            while len(data_bytes)<to_receive:
                by=self.sock.recv(to_receive-len(data_bytes))
                data_bytes+=by
            file_name=data_bytes.decode("utf-8")
            print("File name: ",file_name)
           # sending size of data
            self.sock.sendall(bytes(str(self._files_data[file_name]).ljust(100),"utf-8"))
            # sending data of file
            file="\\store\\"+file_name
            path=os.getcwd()+file
            fp=open(path,"rb");
            bytes_sent=0
            chunk_size=4096
            while bytes_sent<self._files_data[file_name]:
                if(chunk_size>(self._files_data[file_name]-bytes_sent)): chunk_size=self._files_data[file_name]-bytes_sent
                to_send=fp.read(chunk_size)
                self.sock.sendall(to_send)
                bytes_sent+=chunk_size
            fp.close()
            data_bytes=b''
            to_receive=100
            while len(data_bytes)<to_receive:
                by=self.sock.recv(to_receive-len(data_bytes))
                data_bytes+=by
            print("File uploaded !!")
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
    print(sock,socket_name)
    pr=Processor(sock)
