import socket
import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import binascii
import smbus
import threading

def i2cWrite(addr,cmd,data):
    try:
        bus.write_block_data(addr,cmd,data)
    except IOError:
        pass
class GetTitleThread(threading.Thread):
    def __init__(self,i):
        threading.Thread.__init__(self)
    def run(self):
        HOST = ''
        PORT = 7878
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(1)
        vs = PiVideoStream().start()
        #time.sleep(2.0)

        while True:
            print('WAIT FOR PORT 7878')
            conn, addr = sock.accept();

            while True:
                try:
                    frame = vs.read()
                    ret, buff = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
                    data = np.array(buff)
                    stringData = data.tostring()
                    b = binascii.hexlify(stringData)
                    conn.send(b)
                    conn.send(b'\n')
                except socket.error as msg:
                    break


bus = smbus.SMBus(1)
address = 0x04
t= GetTitleThread('GO')
t.start()
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock2.bind(('', 8989))
sock2.listen(1)
while True:
    print('WAIT FOR PORT 8989')
    conn2, addr2 = sock2.accept();
    i2cWrite(address,0x02,[1])
    while True:
        data = conn2.recv(12).decode("utf-8")
        JoyStick = [int(data[i:i+3]) for i in range(0, len(data), 3)]
        if len(JoyStick)!=0:
            i2cWrite(address,0x01,[JoyStick[0],JoyStick[1],JoyStick[2],JoyStick[3]])
        else:
            i2cWrite(address,0x02,[0])
            break
