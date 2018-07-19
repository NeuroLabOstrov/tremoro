# -*- coding: utf8 -*-
from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
import os
import base64
import sqlite3
import json
import time
from threading import Thread


addr = '192.168.43.102'
port_1 = 80
port_2 = 4444

global answer
global file
file = 'data.db'

def get_parent_dir(directory):
    return os.path.dirname(directory)

parent = get_parent_dir(os.getcwd())
os.chdir("{0}/data".format(parent))

#open('data.txt', 'wb').close()                                               #Удаление данных из data

#Create custom HTTPRequestHandler class
class HTTPHandler_esp(BaseHTTPRequestHandler):
    #handle GET command
    def do_GET(self):
        answer = "OK"
        try:
            request = base64.b64decode(self.path[1:].encode()).decode()
        except BaseException:
            request = self.path[1:]
            
        if 'get_esp_1' in request:
            size = int(request.split(' ')[1])
            self.send_esp_data(size,1)
            
        elif 'get_esp_2' in request:
            size = int(request.split(' ')[1])
            self.send_esp_data(size,2)
            
        elif 'get_esp_3' in request:
            size = int(request.split(' ')[1])
            self.send_esp_data(size,3)           
            
        else: 
            if self.client_address[0] == '192.168.43.149':
                store_esp_data(request,1)
                
            elif self.client_address[0] == '':
                store_esp_data(request,2)
                
            elif self.client_address[0] == '':
                store_esp_data(request,3)
            
            #send code 200 response
            self.send_response(200)
            #send header first
            self.send_header('Content-type','text-html')
            self.end_headers()
    
            #send file content to client
            self.wfile.write(answer.encode())
        return
    
    def store_esp_data(self,data,esp_num):
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        time1 = time.time()
        ax,ay,az,gx,gy,gz,emg = data.split(' ')
        data1 = [(time1,esp_num,ax,ay,az,gx,gy,gz,emg)]
        cursor.executemany("INSERT INTO esp(time,esp_num,ax,ay,az,gx,gy,gz,emg) VALUES (?,?,?,?,?,?,?,?,?)", data1)
        conn.commit()
        conn.close()
        
    def send_esp_data(self,size,esp_num):
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        
        sql = "SELECT * FROM esp ORDER BY id DESC LIMIT ? WHERE esp_num = ?"
        cursor.execute(sql,[(size,esp_num)])
        l = cursor.fetchall()
        
        
        arg = ('id','time','esp_num','ax','ay','az','gx','gy','gz','emg')
        dic = [dict(zip(arg,i)) for i in l]
        jsonarray = json.dumps(dic, ensure_ascii=False)
        
        #send code 200 response
        self.send_response(200)
    
        #send header first
        self.send_header('Content-type','application/json')
        self.end_headers()
    
        #send file content to client
        self.wfile.write(jsonarray.encode())
        conn.commit()
        conn.close()
        
class HTTPHandler_opencv(BaseHTTPRequestHandler): 
    answer = "OK"
    def do_GET(self):
        try:
            request = base64.b64decode(self.path[1:].encode()).decode()
        except BaseException:
            request = self.path[1:]
            
        if 'get_opencv' in request:
            size = int(request.split(' ')[1])
            self.send_opencv_data(size)
            
        else:    
            self.store_opencv_data(request)
            #send code 200 response
            self.send_response(200)
        
            #send header first
            self.send_header('Content-type','text-html')
            self.end_headers()
        
            #send file content to client
            self.wfile.write(answer.encode())            
            return
    
    def store_opencv_data(self,data):
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        time1 = time.time()
        x,y = data.split(' ')
        data1 = [(time1,x,y)]
        cursor.executemany("INSERT INTO opencv(time,x,y) VALUES (?,?,?)", data1)
        conn.commit()
        conn.close()     
        
    def send_opencv_data(self,size):
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
        
        sql = "SELECT * FROM opencv ORDER BY id DESC LIMIT ?"
        cursor.execute(sql,[(size)])
        l = cursor.fetchall()
        
        arg = ('id','time','x','y')
        dic = [dict(zip(arg,i)) for i in l]
        jsonarray = json.dumps(dic, ensure_ascii=False)
        
        #send code 200 response
        self.send_response(200)
        
        #send header first
        self.send_header('Content-type','application/json')
        self.end_headers()

        #send file content to client
        self.wfile.write(jsonarray.encode())
        conn.close()    
        

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def serve_on_port_1(port):
    server = ThreadingHTTPServer((addr,port), HTTPHandler_esp)
    server.serve_forever()
    
def serve_on_port_2(port):
    server = ThreadingHTTPServer((addr,port),HTTPHandler_opencv)
    server.serve_forever()

def run():
    print('http server is starting...')

    #ip and port of servr
    #by default http server port is 80
    server_address_1 = (addr, port_1)
    httpd = HTTPServer(server_address_1, HTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()
    
if __name__ == '__main__':
    print('http server is starting...')
    Thread(target=serve_on_port_2, args=[port_2]).start()
    Thread(target=serve_on_port_1, args=[port_1]).start()
    print('http server is running...')
    