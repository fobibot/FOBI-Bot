import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import threading
import time
import socket
import binascii
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

#t= GetTitleThread('GO')
#t.start()
HOST = ''
PORT = 7878
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
vs = PiVideoStream().start()
time.sleep(2.0)
while True:
    try:
        conn, addr = sock.accept();
        frame = vs.read()
        ret, buff = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
        data = np.array(buff)
        stringData = data.tostring()
        print(list(stringData))
        #print(buff)
        b = binascii.hexlify(stringData)
        print(conn.send(stringData))
        conn.send(b'\n')
    except socket.error as msg:
        pass
