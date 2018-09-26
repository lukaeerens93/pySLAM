# Algorithms to be run on raspberry pi in order to read frames from
# the camera and send them to the server. Note the slow frame rate thereupon...
# Frame rate on the receiving end is 2.36 frames per second, may actually
# be quicker to run certain opencv algorithms on raspberry pi, and then send
# a lower dimension, smaller output. 

def piCamWarmup():
    camera = picamera.PiCamera()
    camera.resolution = (300, 200)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)
    return camera



    
def piCamSendFrame(camera, ip, port):
    # Connect a client socket to my_server:8000 (change my_server to the
    # hostname of your server)
    client_socket = socket.socket()
    #enter the IP address of your computer, here is an example IP address
    client_socket.connect((ip, port))

    # Make a file-like object out of the connection
    connection = client_socket.makefile('wb')

    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    stream = io.BytesIO()
    i = 0
    for foo in camera.capture_continuous(stream, 'jpeg'):
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream.read())
        # If we've been capturing for more than 20 seconds, quit
        if i == 1:
            break
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
        i = i + 1
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
    return connection, client_socket, camera



def piCamClose(connection, client_socket, camera):
    connection.close()
    client_socket.close()
    camera.stop_preview()




#============================= Test Code ====================================
import io
import socket
import struct
import time
import picamera
j = 0 
cam = piCamWarmup()
while (True):

    if (j == 100):
        break
    
    c,cs,cam = piCamSendFrame(cam, '172.16.1.191', 8000)
    j = j + 1
piCamClose(c,cs,cam)
