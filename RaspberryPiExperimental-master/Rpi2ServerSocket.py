# Sending Data from Raspberry Pi to PC
import sys
import socket

def socketSend(num, buffer_size,ip, port, policy):
    # Num:              the data you want to send
    # buffer_size:      size of Buffer
    # ip:               IP address of the server
    # port:             Internet Port Number
    # policy:           Whether one way communication (0) or dual way (1)
    tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to IP address of remote PC and specify port number
    # For more details on which port numbers you can choose from:  https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers    
    # in the case of the test: ip = '172.16.1.191' and the portNO = 8000
    tcpsocket.connect((ip, port))

    # Convert into a string
    numstr = str(num)
    
    # Encode unicode string into byte string and send it
    tcpsocket.send(numstr.encode())

    if (policy == 1):
        data = tcpsocket.recv(buffer_size).decode()
        print (data)
        print (type(data))
    tcpsocket.close() 


#============================= Test code ================================
'''

l = [-1,-1]
i = 14
j = 20
l[0],l[1] = 14,20
print (l)

while True:
    
    socketSend(l,20,'172.16.1.191', 8000, 1)
    i = i + 1
    j = j + 1
    l[0],l[1] = i,j
    if (i == 10):
        break
'''
