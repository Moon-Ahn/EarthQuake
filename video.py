import time
import os
import cv2
import imutils
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from threading import Thread


class video(QObject):
    sendImage = pyqtSignal(QImage)

    def __init__(self, widget, size):
        super().__init__()
        self.widget = widget
        self.size = size
        self.sendImage.connect(self.widget.recvImage)

        self.filters = []

    def URL(self,url):
        global Url
        Url = url

    def startCam(self):
        global Url
        try:
            self.cap = cv2.VideoCapture(Url)
            #self.cap = cv2.VideoCapture('rtsp://root:root@192.168.0.250:554/cam0_0')
        except Exception as e:
            print('Cam Error : ', e)
        else:
            self.bThread = True
            self.thread = Thread(target=self.threadFunc)
            self.thread.start()

    def stopCam(self):
        self.bThread = False
        bopen = False
        try:
            bopen = self.cap.isOpened()
        except Exception as e:
            print('Error cam not opened')
        else:
            self.cap.release()

    def threadFunc(self):
        while self.bThread:
            ok, frame = self.cap.read()
            try:
                frame = imutils.resize(frame,width=640)
            except:
                print('pass')
                self.cap = cv2.VideoCapture(Url)
                continue
            if ok:
                # detect image
                try:
                    filename = 'Bounding_Box.txt'
                    r = open(filename, mode='rt', encoding='utf-8')
                    k = r.read()
                    t = k.split(' ')
                    r.close()
                    # os.remove(filename)
                except:
                    t = ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00']
                Box_array = 0
                while Box_array <12 :
                    try:
                        t[Box_array] = int(t[Box_array], 16)*8
                    except:
                        pass
                    Box_array+=1

                try:
                    cv2.rectangle(frame, (t[0], t[1]), (t[0] + t[2], t[1] + t[3]),(0,0,255),1) # FireDetect
                    #print('k')
                    #print(t[0])
                except:
                    cv2.rectangle(frame, (0, 0), (0, 0), (0, 0, 255), 3)  # FireDetect
                    #print('notk')
                try:
                    cv2.rectangle(frame, (t[4], t[5]), (t[4] + t[6], t[5] + t[7]), (255, 255, 255), 1)  # SmokeDetect
                    #print('c')
                except:
                    cv2.rectangle(frame, (0, 0), (0, 0), (255, 255, 255), 3)  # SmokeDetect
                    #print('notc')
                try:
                    cv2.rectangle(frame, (t[8], t[9]), (t[8] + t[10], t[9] + t[11]), (255, 0, 0), 1)  # TestDetect
                    #print('w')
                except:
                    cv2.rectangle(frame, (0, 0), (0, 0), (255, 0, 0), 3)  # SmokeDetect
                    #print('notw')
                #print(t[0])
                #print(t[7])
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                bytesPerLine = ch * w
                img = QImage(rgb.data, w, h, bytesPerLine, QImage.Format_RGB888)
                resizedImg = img.scaled(self.size.width(), self.size.height(), Qt.KeepAspectRatio)
                self.sendImage.emit(resizedImg)
            else:
                print('cam read error')

            time.sleep(0.01)

        print('thread finished')
