# RaspberryPi
Code to be only run on the raspberry pi extension

Table of Contents:
1. Pre-Requisite Tutorials
2. Explanation of Files in Repository
____________________________________________________________________________________________________________________________________
1) Pre-Requisite Tutorials:

Setting up a Firewall

In order to access a brand new raspberry pi (model 2 or older) remotely through SSH or through VNC, you will need to create a firewall. The most convenient way to do this is through uncomplicated firewall (UFW) which can be implemented very easily through terminal in the raspberry pi.


The first step is to install UFW:
```
sudo apt-get install ufw
```

The second step is to install the default settings of the firewall:
```
sudo ufw default deny incoming
```
```
sudo ufw default allow outgoing 
```

The third step is to allow SSH connections:
```sudo ufw allow ssh```

(Optional) if you want to configure your SSH daemon to listen to only a specific port such as port number 2222:
```
sudo ufw allow 2222
```


The fourth step is to enable the UFW:
```
sudo ufw enable
```


All done!  You now should be able to connect to the raspberry pi remotely through SSH. If you would like to check on the status of the UFW, run:
```
sudo ufw status verbose
```


All the above represents a summary of the article published on Digital Ocean by Mitchell Anicas:
https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04
and Shaun Lewis:
https://www.digitalocean.com/community/tutorials/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server

Both of these articles are essentially the same with slightly more detail and information from Mitchell Anicas. For more advanced users who wish to experiment a little bit more with UFW, please visit these articles, for beginners the above instructions should do.




Setting up VNC

The following link is filled with everything that you need to know about using VNC to connect remotely to the raspberry pi: https://www.raspberrypi.org/documentation/remote-access/vnc/

A summarization of the content is not provided because of how concise and easy to follow the instructions are in the link.





Accessing Raspberry Pi (with different IP address) through SSH from the same PC

Students who will connect the raspberry pi to the same wifi but different server and attempt to access this raspberry pi remotely through SSH from the server will experience an error as described here: https://stackoverflow.com/questions/20840012/ssh-remote-host-identification-has-changed
 
As found in the document the solution is to simply write the following in the terminal of the host PC/ server: 

```
ssh-keygen -R <host>
```

where the <host> is simply the IP address of the server. So you could write it as:

```
ssh-keygen -R 192.168.3.10
```
Provided that your server IP address is: 192.168.3.10

If you are unsure what the IP address of your server is: 
If mac/linux enter in terminal: 

```
ifconfig
```

The nature of the problem is excellently described by one of the commenters to this stackoverflow page: 
“The problem is that you've previously accepted an SSH connection to a remote computer and that remote computer's digital fingerprint or SHA256 hash key has changed since you last connected. Thus when you try to SSH again or use github to pull code, which also uses SSH, you get an error. Why? Because you're using the same remote computer address as before but the remote computer is responding with a different fingerprint. Therefore, it's possible that someone is spoofing the computer you previously connected to. This is a security issue.”anon58192932

____________________________________________________________________________________________________________________________________
2) Explanation of Files in Repository

---Rpi2ServerSocket.py--- (Used in conjunction with receiveDataFromRpi.py (SLAM repository) on the PC side)
Contains a function called socketSend that when implemented sends data from the raspberry pi to the PC. Also contains a test script for this socketSend function that sends an array of 2 numbers, both of which change by differing amounts at runtime.

---imageSendRPi.py--- (Used in confunction with PiCamServerReceive.py (SLAM repository) on the PC side)
Contains 3 functions (one for warming up the picamera, one for sending frames to the PC wirelessly, and the other for closing the picamera). Along with this is a test script that sends 100 sequential frames from the camera to a remote PC, and then closes the picamera.

---ultrasonicRangeRPi.py---
Contains many functions that are used in order to make use of the ultrasonic range finder sensors. There is a test script included which shows how to use all of these together.

---TestRPiUltraSend.py---
Simply pairs the ultrasonicRangeRpi test script with the Rpi2ServerSocket test script in order to send the ultrasound values to the PC. This file only exists because PCB was not working yet and so Raspberry Pi relayed information to a remote PC for testing Finch 2.0 software.

---UltrasoundEvasion.py---
Tests collision avoidance based on ultrasonic range finder. Steers away based on SPEED not distance. Imports ultrasonicRangeRpi so make sure that you comment out the test script of ultrasonicRangeRpi to avoid running its test script instead of this one.
