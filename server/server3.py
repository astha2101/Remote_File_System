import socket
from threading import Thread,Semaphore
import sys
import os
from uuid import uuid1
class Model():
    def __init__(self):
        self.files=os.listdir('c:\pyeg\proj1\server\store')
        self.files_data=dict()
        self.uname_pwd=dict()
        self.uid_uname=dict()
        self.file_semaphore=dict()
        for i in self.files:
            file="\\store\\"+i
            path=os.getcwd()+file
            self.files_data[i]=os.path.getsize(path)
            self.file_semaphore[i]=Semaphore(2)
        file=open("users.txt",'rb')
        while True:
            a=file.readline()
            if len(a)==0: break
            t=eval(a)
            print(t)
            self.uname_pwd[t[0]]=t[1]
        file.close()
        
class Processor(Thread):
    def __init__(self,sock,model):
        Thread.__init__(self)
        self.sock=sock
        self.model=model
        self.start()
    def run(self):
            data_bytes=b''
            to_receive=100
            # receiving length of request string
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
            request_tuple=eval(request)
            print("Request received as ",request)
            ack="12"
            self.sock.sendall(bytes(ack,"utf-8"))
            if request_tuple[0]=="shutdown":
                os._exit(0)
                sys.exit()
            if request_tuple[0]=="login":
                #receiving length of string containing username and password
                data_bytes=b''
                to_receive=100
                while len(data_bytes)<to_receive:
                    by=self.sock.recv(to_receive-len(data_bytes))
                    data_bytes+=by
                ack="12"
                self.sock.sendall(bytes(ack,"utf-8"))
                uname_pwd_length=int(data_bytes.decode("utf-8").strip())
                to_receive=uname_pwd_length
                data_bytes=b''
                while len(data_bytes)<to_receive:
                    by=self.sock.recv(to_receive-len(data_bytes))
                    data_bytes+=by
                ack="12"
                self.sock.sendall(bytes(ack,"utf-8"))
                uname_pwd_string=data_bytes.decode("utf-8")
                t=eval(uname_pwd_string)
                response='("Incorrect"," ")'
                if t[0]  in self.model.uname_pwd:
                    if t[1]==self.model.uname_pwd[t[0]]:
                        a=uuid1()
                        uid=str(a)
                        response='("Correct","'+uid+'")'
                        self.model.uid_uname[uid]=t[0]
                #sending response                      
                self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8"))           
                self.sock.sendall(bytes(response,"utf-8"))
                print("loging done")
                return
            if request_tuple[0]=="dir":
                response="Valid"
                if request_tuple[1] not in self.model.uid_uname.keys():
                    response="Invalid"
                    self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8"))           
                    self.sock.sendall(bytes(response,"utf-8"))
                    return
                self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8"))           
                self.sock.sendall(bytes(response,"utf-8")) 
                # sending number of files
                self.sock.sendall(bytes(str(len(self.model.files)).ljust(100),"utf-8"))
                # sending files name        
                for i in self.model.files:
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
                return        
            if request_tuple[0]=="find":
                response="Valid"
                if request_tuple[1] not in self.model.uid_uname.keys():
                    response="Invalid"
                    self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8"))           
                    self.sock.sendall(bytes(response,"utf-8"))
                    return
                self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8"))           
                self.sock.sendall(bytes(response,"utf-8")) 
                # receiving length of file name
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
                if file_name not in self.model.files_data:
                    response="INVALID"
                    self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8")) 
                    self.sock.sendall(bytes(response,"utf-8"))
                    return
                response="VALID" 
                self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8")) 
                self.sock.sendall(bytes(response,"utf-8"))
            if request_tuple[0]=="add":
                data_bytes=b''
                to_receive=100
                while len(data_bytes)<to_receive:
                    by=self.sock.recv(to_receive-len(data_bytes))
                    data_bytes+=by
                file_name_length=int(data_bytes.decode("utf-8").strip())   
                data_bytes=b''
                to_receive=file_name_length
                while len(data_bytes)<to_receive:
                    by=self.sock.recv(to_receive-len(data_bytes))
                    data_bytes+=by
                fileName=data_bytes.decode("utf-8")
                self.sock.sendall(bytes(ack,"utf-8"))
                filepath=os.path.join('c:\pyeg\proj1\server\store',fileName)
                file=open(filepath,"wb")
                data_bytes=b''
                to_receive=100
                while len(data_bytes)<to_receive:
                    by=self.sock.recv(to_receive-len(data_bytes))
                    data_bytes+=by
                file_length=int(data_bytes.decode("utf-8").strip())    
                data_bytes=b''
                to_receive=file_length
                while len(data_bytes)<to_receive:
                    by=self.sock.recv(to_receive-len(data_bytes))
                    data_bytes+=by
                    file.write(by)
                file.close() 
                self.model.files.append(fileName)
                self.model.files_data[fileName]=file_length
                print("File received") 
                response="File added to the store successfully !"
                self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8"))
                self.sock.sendall(bytes(response,"utf-8"))                
            if request_tuple[0]=="delete":
                data_bytes=b''
                to_receive=100
                while len(data_bytes)<to_receive:
                    by=self.sock.recv(to_receive-len(data_bytes))
                    data_bytes+=by
                file_name_length=int(data_bytes.decode("utf-8").strip())   
                data_bytes=b''
                to_receive=file_name_length
                while len(data_bytes)<to_receive:
                    by=self.sock.recv(to_receive-len(data_bytes))
                    data_bytes+=by
                fileName=data_bytes.decode("utf-8")
                self.sock.sendall(bytes(ack,"utf-8"))
                filePath="C:\\pyeg\\proj1\\server\\store\\"+fileName
                os.remove(filePath)
                self.model.files_data.pop(fileName)
                self.model.files.remove(fileName)
                response="File is successfully deleted from the store !!"
                self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8"))
                self.sock.sendall(bytes(response,"utf-8"))  
            if request_tuple[0]=="get":
                response="Valid"
                if request_tuple[1] not in self.model.uid_uname.keys():
                    response="Invalid"
                    self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8"))           
                    self.sock.sendall(bytes(response,"utf-8"))
                    return
                self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8"))           
                self.sock.sendall(bytes(response,"utf-8")) 
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
                self.sock.sendall(bytes(str(self.model.files_data[file_name]).ljust(100),"utf-8"))
                # sending data of file
                file="\\store\\"+file_name
                path=os.getcwd()+file
                fp=open(path,"rb");
                bytes_sent=0
                chunk_size=4096
                self.model.file_semaphore[file_name].acquire()
                while bytes_sent<self.model.files_data[file_name]:
                    if(chunk_size>(self.model.files_data[file_name]-bytes_sent)): chunk_size=self.model.files_data[file_name]-bytes_sent
                    to_send=fp.read(chunk_size)
                    self.sock.sendall(to_send)
                    bytes_sent+=chunk_size
                fp.close()
                self.model.file_semaphore[file_name].release()
                print("File uploaded !!")
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
                return
            if request_tuple[0]=="logout":
                self.model.uid_uname.pop(request_tuple[1])
                response="User logged out"
                self.sock.sendall(bytes(str(len(response)).ljust(100),"utf-8")) 
                self.sock.sendall(bytes(response,"utf-8"))

serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(("localhost",5500))
serverSocket.listen()
model=Model()
while True:
    print("Server is in listening mode")
    sock,socket_name=serverSocket.accept()
    pr=Processor(sock,model)
