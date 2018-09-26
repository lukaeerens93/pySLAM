# To be ran on the server/ remote PC or by the Finch (haven't tested direct
# RPi to Finch communication without passing through a PC first 

def socketReceive(buffer_size, ip, port, echo):
    # buffer_size:      Size of Buffer
    # ip:               ip address of server (which should be "0.0.0.0")
    # port:             Internet Port Number
    # echo:             Send signal back to the raspberry pi (1) or not (0)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind( (ip, port) ) 
        
    s.listen(2)
    (client, (ip,port) ) = s.accept()

    print "received connection from %s" %ip
    print " and port number %d" %port

    data = client.recv(20).decode()

    print data
    if (echo == 1):
        client.send(data.encode())
    s.close()
    return data



def socketDualWay(num, buffer_size, ip, port, echo):
    # num:              Datasample that you will send to the raspberry pi
    # buffer_size:      Size of Buffer
    # ip:               ip address of server (which should be "0.0.0.0")
    # port:             Internet Port Number
    # echo:             Send signal back to the raspberry pi (1) or not (0)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind( (ip, port) ) 
        
    s.listen(2)
    (client, (ip,port) ) = s.accept()

    print "received connection from %s" %ip
    print " and port number %d" %port

    data = client.recv(20).decode()
    print data

    numstr = str(num)
    if (echo == 1):
        client.send(numstr.encode())
    s.close()
    return data

# =============================== Test Code =====================================
import socket

data = [-99,-99]

k,i = 0,0

while (True):
    # You could comment the next 2 lines out if you just want to test socketDualWay
    # d = socketReceive(20, "0.0.0.0", 8000, 1)
    # print ("data: " + str(d))

    # You could comment the next 2 lines out if you just want to test socketReceive
    d = socketDualWay(data, 20, "0.0.0.0", 8000, 1)
    print ("data: " + str(d))

    data[0] = i
    
    
    k = k + 1
    i = i - 1
    if (k == 9):
        break



