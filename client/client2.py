import socket
import os
import sys

class TMClient:
    def __init__(self):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(("localhost",5500))
    def __del__(self):
        self.socket.close()
    def processDir(self):
        request="dir"
        self.socket.sendall(bytes(str(len(request)).ljust(100),"utf-8"))
        data_bytes=b''
        to_receive=2
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        ack=data_bytes.decode("utf-8")
        #sending request 
        self.socket.sendall(bytes(request,"utf-8"))
        data_bytes=b''
        to_receive=2
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        ack=data_bytes.decode("utf-8").strip()
        #receiving number of files
        data_bytes=b''
        to_receive=100
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        number_of_files=int(data_bytes.decode("utf-8").strip())
        files=[]
        for i in range(number_of_files):
            data_bytes=b''
            to_receive=100
            while len(data_bytes)<to_receive:
                by=self.socket.recv(to_receive-len(data_bytes))
                data_bytes+=by
            length_of_file_name=int(data_bytes.decode("utf-8").strip())
            data_bytes=b''
            to_receive=length_of_file_name
            while len(data_bytes)<to_receive:
                by=self.socket.recv(to_receive-len(data_bytes))
                data_bytes+=by
            file_name=data_bytes.decode("utf-8")
            files.append(file_name)
            ack="12"
            self.socket.sendall(bytes(ack,"utf-8"))
        response="All files received !!"
        self.socket.sendall(bytes(str(len(response)).ljust(100),"utf-8"))
        self.socket.sendall(bytes(response,"utf-8"))
        return files
    def canProcess(self,file_name):
        request="find"
        #sending length of request
        self.socket.sendall(bytes(str(len(request)).ljust(100),"utf-8"))
        data_bytes=b''
        to_receive=2
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        ack=data_bytes.decode("utf-8")
        #sending request 
        self.socket.sendall(bytes(request,"utf-8"))
        data_bytes=b''
        to_receive=2
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        ack=data_bytes.decode("utf-8").strip()    
        #sending file name size
        self.socket.sendall(bytes(str(len(file_name)).ljust(100),"utf-8"))
        #sending file name 
        self.socket.sendall(bytes(file_name,"utf-8"))
        data_bytes=b''
        to_receive=100
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        response_length=int(data_bytes.decode("utf-8").strip())   
        data_bytes=b''
        to_receive=response_length
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        response=data_bytes.decode("utf-8")
        return response
    def processGet(self,file_name,new_file_name):
        request="get"
        self.socket.sendall(bytes(str(len(request)).ljust(100),"utf-8"))
        data_bytes=b''
        to_receive=2
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        ack=data_bytes.decode("utf-8")
        #sending request 
        self.socket.sendall(bytes(request,"utf-8"))
        data_bytes=b''
        to_receive=2
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        ack=data_bytes.decode("utf-8").strip()
        #sending file name size
        self.socket.sendall(bytes(str(len(file_name)).ljust(100),"utf-8"))
        #sending file name 
        self.socket.sendall(bytes(file_name,"utf-8"))
        file=open(new_file_name,"wb")
        data_bytes=b''
        to_receive=100
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        file_length=int(data_bytes.decode("utf-8").strip())    
        print(file_length)
        data_bytes=b''
        to_receive=file_length
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
            file.write(by)
        file.close()
        response="File received !"
        self.socket.sendall(bytes(str(len(response)),"utf-8"))
        self.socket.sendall(bytes(response,"utf-8"))
        return "File downloaded !!!"       
 

while True:
    request=input("tmclient->")
    request.strip()
    if len(request)==0:
        print("Invalid command")
        continue
    if request.lower()=='quit':
        break
    elif request.lower()=='dir':
        tmClient=TMClient()
        files=tmClient.processDir()
        for i in files:
            print(i)
    elif request.lower().startswith("get"):
        if len(request)==3:
            print("Invalid command")
            continue
        parts=request.split("get")
        print(parts)
        tmClient=TMClient()
        file_exists=tmClient.canProcess(parts[1].strip())
        if file_exists=="INVALID": print("Invalid file name :",parts[1])
        else:
            new_file_name=input("Save as ")
            if len(new_file_name)==0: new_file_name=parts[1].strip()
            tmClient=TMClient()
            msg=tmClient.processGet(parts[1].strip(),new_file_name)
            print(msg) 

        
        

