# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 10:18:49 2018

@author: izaia
"""

from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import os
import socket  # BSD socket interface
import sys  # access system arguments with sys.argv and use sys.exit() to provide Unix exit codes


def start_server(port):
    import socket
    # ******1. Initialize server with port, host, and directory where serving files are stored ******
    
    host = 'localhost'
    port = port
    
    # Directory where webpage files are stored
    wdir = 'C:\\Users\\izaia\\.spyder\\Project1\\file_directory\\' 
    
    # 2. Attempt to aquire the socdet and launch the server

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        
        
        print("Launching HTTP server on ", host, ":", port) 
        server_socket.bind(("", port)) #Remember we are using just the quotes vs "local host" so that we may listen from any client
     
    except Exception as e:
        
        print("ERROR: Failed to acquire sockets for port ", port)
        print("Try running the Server in a privileged user mode.")
        shutdown(server_socket)
        sys.exit(1)
    
    #3 listen and wait for connection
    """ Main loop awaiting connections """

    while True:

         print ("Waiting for New Connection")
         
         #(conn, addr) = self.socket.accept()
         server_socket.listen(1) # maximum number of queued connections
         (conn, addr) = server_socket.accept()
          
         
         # conn - socket to client

        # addr - clients address


         print("Made connection with client from:", addr)

         data = conn.recv(1024) #receive data from client
         string = bytes.decode(data) #decode it to string

         #determine request method  (Only GET is supported)

         request_method = string.split(' ')[0]
         print ("Method: ", request_method)
         print ("Request body: ", string)

 
         #if string[0:3] == 'GET':

         if (request_method == 'GET'):
             
             RequestedFile = string.split(' ')
             RequestedFile =  RequestedFile[1] # get 2nd element

 

             #Check for URL arguments. Disregard them

             RequestedFile =  RequestedFile.split('?')[0]  # disregard anything after '?'

             if ( RequestedFile == '/'):  # in case no file is specified by the browser
                  RequestedFile = '/index.html' # load index.html by default

 
             RequestedFile = wdir + RequestedFile

             print ("Serving web page [", RequestedFile,"]")

 

             ## Load file content

             try:

                 file_var = open( RequestedFile,'rb')

                 if (request_method == 'GET'):  #only read the file when GET

                     ResponseContent = file_var.read() # read file content

                 file_var.close()
                 ResponseHeader = create_headers( 200)

 
             except Exception as e: #in case file was not found, generate 404 page

                 print ("Warning, file not found. Serving response code 404\n", e)

                 ResponseHeader = create_headers( 404)

 
                 #if (request_method == 'GET'):

                    #response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"
             
                
            # Need to implement exception for 403 forbidden
 

             ServerResponse =  ResponseHeader.encode() # return headers for GET and HEAD

             if (request_method == 'GET'):

                 ServerResponse +=  ResponseContent  # return additional conten for GET only

 

             conn.send(ServerResponse)

             print ("Closing connection with client")

             conn.close()

 

         else:

             print("Unknown HTTP request method:", request_method)
   
   
def create_headers(code):

     """ Generates HTTP response Headers. Ommits the first line! """

 
     # determine response code

     h = ''

     if (code == 200):
         h = 'HTTP/1.1 200 OK\n'
        
     elif(code == 404):
         h = 'HTTP/1.1 404 Not Found\n'

     # Still need to implement 403 forbidden response 
     return h   
   
def shutdown(sock):
     """ Shut down the server """

     try:

         print("Server Shutting Down")
         sock.shutdown(socket.SHUT_RDWR)

     except Exception as e:
         
         print("Warning: Failed to shut down the socket", e)   

#Shuts server down on Ctrl + c
import signal 
signal.signal(signal.SIGINT, shutdown)
     
     
     
def main():
    # check that 1 argument is given in addition to the .py file name
    # if so, attempt an HTTP GET request using the argument as the address
    # if not, exit with a non-zero exit code
    if len(sys.argv) == 2:
        
        start_server(sys.argv[1])
    else:
        sys.exit('Must provide 1 address argument')


if __name__ == '__main__':
    main()     