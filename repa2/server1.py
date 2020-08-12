import socket

def fact(n):
        if n==0: return 1
        return n*fact(n-1)


# next create a socket object 
s = socket.socket()
print("Socket successfully created")

# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 8081
  
s.bind(('', port))         
print("socket binded to %s" %(port)) 
  
# put the socket into listening mode 
s.listen(5)      
print("socket is listening")            
  
# a forever loop until we interrupt it or  
# an error occurs 
c, addr = s.accept()
while True:
   # Establish connection with client.       
        print('Got connection from', addr)
        print(c.recv(1024))
        #for i in range(0, 20000):
        #val = fact(300)
        #c.send(repr(val).encode('utf-8'))
   # send a thank you message to the client.  
        c.send('Thank you for connecting'.encode())

   # Close the connection with the client 
        #c.close()

