import socket
import os
import sys

class TMClient:
    def __init__(self):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(("localhost",5500))
        self.uid=""
    def __del__(self):
        self.socket.close()
    def login(self,username,password):
        request='("login",0)'
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
        #sending username and password
        uname_pwd='("'+str(username)+'","'+str(password)+'")'
        self.socket.sendall(bytes(str(len(uname_pwd)).ljust(100),"utf-8"))
        data_bytes=b''
        to_receive=2
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        ack=data_bytes.decode("utf-8") 
        self.socket.sendall(bytes(uname_pwd,"utf-8"))
        data_bytes=b''
        to_receive=2
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        ack=data_bytes.decode("utf-8").strip()
        # receiving response
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
        response_tuple=eval(response)
        if response_tuple[0]=="Incorrect": return False
        self.uid=response_tuple[1]
        return True 
    def processDir(self):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(("localhost",5500)) 
        request='("dir","'+self.uid+'")'
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
        if response=="Invalid": return
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
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(("localhost",5500))
        request='("find","'+self.uid+'")'
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
        if response=="Invalid": return  
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
    def processAdd(self,fileName):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(("localhost",5500))
        request='("add","'+self.uid+'")'
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
        # send file name and its size
        self.socket.sendall(bytes(str(len(fileName)).ljust(100),"utf-8"))
        self.socket.sendall(bytes(fileName,"utf-8"))
        data_bytes=b''
        to_receive=2
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        ack=data_bytes.decode("utf-8").strip() 
        path=os.getcwd()+"\\"+fileName
        fileSize=os.path.getsize(path)
        # sending size of the file
        self.socket.sendall(bytes(str(fileSize).ljust(100),"utf-8"))
        # sending file data
        fp=open(path,"rb");
        bytes_sent=0
        chunk_size=4096
        while bytes_sent<fileSize:
            if(chunk_size>(fileSize-bytes_sent)): chunk_size=fileSize-bytes_sent
            to_send=fp.read(chunk_size)
            self.socket.sendall(to_send)
            bytes_sent+=chunk_size
        fp.close()        
        data_bytes=b''
        to_receive=100
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        response_length=int(data_bytes.decode("utf-8").strip())
        to_receive=response_length
        data_bytes=b''
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        response=data_bytes.decode("utf-8")
        return response
    def processDelete(self,file_name):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(("localhost",5500))
        request='("delete","'+self.uid+'")'
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
        # sending file name and its length
        self.socket.sendall(bytes(str(len(file_name)).ljust(100),"utf-8"))
        self.socket.sendall(bytes(file_name,"utf-8"))
        data_bytes=b''
        to_receive=2
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        ack=data_bytes.decode("utf-8").strip() 
        data_bytes=b''
        to_receive=100
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        response_length=int(data_bytes.decode("utf-8").strip())
        to_receive=response_length
        data_bytes=b''
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
        response=data_bytes.decode("utf-8")
        return response   
    def processGet(self,file_name,new_file_name):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(("localhost",5500))
        request='("get","'+self.uid+'")'
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
        if response=="Invalid": return
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
        data_bytes=b''
        to_receive=file_length
        print("Waiting to download .............")
        while len(data_bytes)<to_receive:
            by=self.socket.recv(to_receive-len(data_bytes))
            data_bytes+=by
            file.write(by)
            percentage=int((len(data_bytes)/to_receive)*100)
            print("Progress:- "+str(percentage)+"% completed.")
        file.close()
        response="File received !"
        self.socket.sendall(bytes(str(len(response)),"utf-8"))
        self.socket.sendall(bytes(response,"utf-8"))
        return "File downloaded !!!"   
    def logout(self):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(("localhost",5500))
        request='("logout","'+self.uid+'")'
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
        # receiving response
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


      
while True:
    username=input("tmclient->Username ")
    username.strip()
    password=input("tmclient->Password ")
    password.strip()
    tmClient=TMClient()
    if tmClient.login(username,password)==False:
        print("Invalid username/password")
        sys.exit()
    else: break;
while True:
    request=input("tmclient->")
    request.strip()
    if len(request)==0:
        print("Invalid command")
        continue
    if request.lower()=='quit':
        tmClient.logout()
        break
    elif request.lower()=='dir':
        files=tmClient.processDir()
        for i in files:
            print(i)
    elif request.lower().startswith("get"):
        if len(request)==3:
            print("Invalid command")
            continue
        parts=request.split("get")
        file_exists=tmClient.canProcess(parts[1].strip())
        if file_exists=="INVALID": print("Invalid file name :",parts[1])
        else:
            new_file_name=input("Save as ")
            if len(new_file_name)==0: new_file_name=parts[1].strip()
            msg=tmClient.processGet(parts[1].strip(),new_file_name)
            print(msg) 
    elif request.lower().startswith("add"):
        if len(request)==3:
            print("Invalid command")
            continue
        parts=request.split("add")
        msg=tmClient.processAdd(parts[1].strip())
        print(msg)
    elif request.lower().startswith("delete"):
        if len(request)==3: 
            print("Invalid command")
            continue
        parts=request.split("delete")
        file_exists=tmClient.canProcess(parts[1].strip())
        if file_exists=="INVALID": print("Invalid file name :",parts[1])
        else:
            canDelete=input("Are you sure you want to delete this file (Y/N) ?")
            if canDelete=="Y" or canDelete=="y":
                msg=tmClient.processDelete(parts[1].strip())
                print(msg)        

