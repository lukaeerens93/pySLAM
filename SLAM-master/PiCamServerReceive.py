# Test Code for server receiving the PiCamera frames.
# This test code combined with the test code from camera.py file
# sends one frame at a time to the PC, this frame being saved as PiCam.bmp
# You can thus take the DNA both of this test code and of other computer 
# vision codes in order to to image processing operations on the PiCam frames

def piCamSetup(ip, port):
    server_socket = socket.socket()
    server_socket.bind((ip, port))
    server_socket.listen(0)
    return server_socket



def piCamReceive(server_socket, verbose):
    # This function reads you one frame from the PiCam so that you can use it as the frame
    # in the while loop of main code which is referred to by the computer vision algorithms.

    connection = server_socket.accept()[0].makefile('rb')

    trigger = 0     # Used to trigger (1) the break of the main function loop if not image_len, or not (0)
    
    image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
    if not image_len:
        trigger = 1
        
    if (trigger != 1):
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)
        image = Image.open(image_stream)

        if (verbose == 1):
            print('Image is %dx%d' % image.size)

        image.save("PiCam.bmp")
        cv2.waitKey(1)
        image.verify()
        if (verbose == 1):
            print("Image is verified")

    return trigger, connection



def piCamCloseConnection(connection, server_socket):                
    connection.close()
    server_socket.close()

        
#============================= Test Code =================================
import io
import socket
import struct
from PIL import Image, ImageTk
import numpy
import cv2

j = 0
ss = piCamSetup('0.0.0.0', 8000)
while True:
    if (j == 100):
        break
    t,c = piCamReceive(ss, 1)
    if (t == 1):
        break
piCamCloseConnection(c,ss)

