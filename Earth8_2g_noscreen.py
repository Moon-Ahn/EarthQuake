import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
import io,csv
from video import *
#from ScreenShot import *

global plottext
plottext =  r'$\vec a _\max= 0.01m/s^2$'
#global Filenumber
#Filenumber = 0
global Line
Line = 0
global array
array = 0
k = 0
global Max_Value
Max_Value=0
global Initial_value
Initial_value = 0
global Initial_x , Initial_y , Initial_z , x_value, y_value , z_value, Sensitivity_Value, count, t1_x,\
    t1_y, t1_z, t2_x, t2_y, t2_z, limit,CycleX_count,CycleY_count,CycleZ_count,CheckPoint_X,CheckPoint_Y,CheckPoint_Z, Scale_count, Scale_value,table_Count
Initial_x = 0
Initial_y = 0
Initial_z = 0
x_value = 0
y_value = 0
z_value = 0
Sensitivity_Value = 0
count = 0
t1_x = 1
t1_y = 1
t1_z = 1
t2_x = 2
t2_y = 2
t2_z = 2
limit = 0.024
CycleX_count = 0
CycleY_count = 0
CycleZ_count = 0
CheckPoint_X = 0
CheckPoint_Y = 0
CheckPoint_Z = 0
Scale_count = 0
Scale_value = 0
table_Count = 0

if len(sys.argv) != 4:
    print("Insufficient Argument")
    sys.exit()

Rtsp = 'rtsp://'+ sys.argv[2] + ':' + sys.argv[3] + '@' \
                   + sys.argv[1] + ':554/cam0_0'

#while k < 3:  # 파일 지우고 체크


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = plt.figure()
        fig = Figure(figsize=(5, 3), dpi=dpi)
        self.axes = fig.add_subplot(111, xlim=(0, 500), ylim=(-2, 2))
        #fig.text(0.48, 0.15, 'ax=')
        self.axes.grid(True,axis='y',linestyle='--')
        fig.text(0.93, 0.93, r'$[g]$', fontdict={'size': 10})
        #fig.text(0.80, 0.80, r'$[m/s^2]$', fontdict={'size': 12})
        fig.text(0.1, 0.1, r'$[s]$', fontdict={'size': 10})
        self.axes.set_xticklabels(["50","40","30","20","10","0"])
        self.axes.figure.tight_layout(pad=0)
        #self.axes2 = fig.add_subplot(212, xlim=(0, 4000), ylim=(0, 600))
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
    def compute_initial_figure(self):
        pass

class AnimationWidget(QWidget):
    def __init__(self):
        ##############################################################
        super().__init__()
        size = QSize(640, 800)
        self.initUI(size)
        self.video = video(self, QSize(self.frm.width(), self.frm.height()))
        ##############################################################

    def initUI(self,size):
        QMainWindow.__init__(self)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox2 = QVBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        vbox1 = QVBoxLayout()
        hbox4 = QHBoxLayout()
        vbox3 = QVBoxLayout()
        vbox4 = QVBoxLayout()
        hbox5 = QHBoxLayout()
        #######################
        #self.setStyleSheet('background-color: #FFFFFF')
        self.frm = QLabel(self)
        self.frm.setFrameShape(QFrame.Panel)
        self.frm.setFixedSize(640, 480)
        #######button#######
        self.start_button = QPushButton("start", self)
        self.stop_button = QPushButton("stop", self)
        self.btn = QPushButton('start cam', self)
        self.btn.setCheckable(True)
        self.start_button.setFixedHeight(50)
        self.stop_button.setFixedHeight(50)
        self.btn.setFixedHeight(50)
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        self.btn.clicked.connect(self.onoffCam)

        self.start_button.setMaximumHeight(300)
        hbox2.addWidget(self.btn)
        hbox2.addWidget(self.start_button)
        hbox2.addWidget(self.stop_button)
        # vbox.addLayout(vbox)
        # hbox.addLayout(hbox)
        vbox1.addWidget(self.frm)
        vbox1.addLayout(hbox2)
        hbox.addLayout(vbox1) #h1

        self.setGeometry(300,150,1370,510)
        self.setFixedSize(1370, 560)
        #self.setFixedSize(size)
        #self.move(600, 100)
        self.setWindowTitle('EarthQuake')
        self.show()
        #######################

        # self.Alarm = QLabel('       ',self)
        # self.Alarm.setFixedSize(700,70)
        # self.Alarm.setStyleSheet("background-color: #7FFFD4")
        self.canvas = MyMplCanvas(self, width=10, height=0, dpi=100)
        #hbox = QHBoxLayout()
        # self.xyz = QLabel(self)
        # pixmap = QPixmap("xyz.png")
        # self.xyz.setPixmap(QPixmap(pixmap))

        self.Detect_Value = QComboBox(self)
        self.Detect_Value.setEditable(True)
        self.Detect_Value.lineEdit().setReadOnly(True)
        self.Detect_Value.lineEdit().setAlignment(Qt.AlignCenter)
        self.Detect_Value.addItem("경진 : ( 0.005g ~ 0.024g )")
        self.Detect_Value.addItem("약진 : ( 0.024g ~ 0.067g )")
        self.Detect_Value.addItem("중진 : ( 0.067g ~ 0.13g )")
        self.Detect_Value.addItem("약강진 : ( 0.13g ~ 0.24g )")
        self.Detect_Value.addItem("강강진 : ( 0.24g ~ 0.44g )")
        self.Detect_Value.addItem("약열진 : ( 0.44g ~ 0.83g )")
        self.Detect_Value.addItem("강열진 : ( 0.83g ~ 1.56g )")
        self.Detect_Value.addItem("격진 : ( 1.56g ~ )")

        #print(self.Detect_Value.currentIndex())
        #self.Detect_Value.setFixedSize(250,25)
        #vbox2.addWidget(self.xyz)
        self.Change_button = QPushButton("Change", self)
        self.Change_button.setFixedSize(70,20)
        self.Change_button.clicked.connect(self.Limit)

        self.sensitivity = QLabel(' Sensitivity:        ',self)
        self.sensitivity.setFont(QFont('Consolas', 14))
        self.Max = QLabel('  MAX:    ', self)
        self.Max.setFont(QFont('Consolas', 14))
        # self.Average = QLabel('Average:         ', self)
        # self.Average.setFont(QFont('Arial', 15))
        hbox3.addWidget(self.Detect_Value)
        hbox3.addWidget(self.Change_button)
        hbox3.addWidget(self.sensitivity)
        hbox3.addWidget(self.Max)
        #hbox3.addWidget(self.Average)

        self.Scale = QLabel('  Scale:      ', self)
        self.Scale.setFont(QFont('Consolas', 14))
        self.Cycle = QLabel('  Cycle      ', self)
        self.Cycle.setFont(QFont('Consolas', 14))
        self.X = QLabel('    X:      ', self)
        self.X.setFont(QFont('Consolas', 14))
        self.Y = QLabel('    Y:      ', self)
        self.Y.setFont(QFont('Consolas', 14))
        self.Z = QLabel('    Z:      ', self)
        self.Z.setFont(QFont('Consolas', 14))



        ###############표(테이블) 삽입#################

        self.table = QTableWidget()
        self.table.setRowCount(1000)
        self.table.setColumnCount(4)
        self.table.setFixedSize(500,180)
        self.table.setAlternatingRowColors(True)
        self.table.setHorizontalHeaderLabels(['시간','진도','주기','크기'])
        self.table.setColumnWidth(2,140)

        self.ResetTable_button = QPushButton("Reset_Table", self)
        self.ResetTable_button.setFixedHeight(30)
        self.ResetTable_button.clicked.connect(self.ResetTable)

        self.SaveExcel_button = QPushButton("Save_Excel", self)
        self.SaveExcel_button.setFixedHeight(30)
        self.SaveExcel_button.clicked.connect(self.WriteCsv)
        # #표에 데이터 삽입
        # item = QTableWidgetItem("201409072")
        # item.setTextAlignment(Qt.AlignCenter)
        # self.table.setItem(0,0,item)
        # item = QTableWidgetItem("진도")
        # item.setTextAlignment(Qt.AlignCenter)
        # self.table.setItem(0, 1, item)

        ######################################

        vbox3.addWidget(self.Scale)
        vbox3.addWidget(self.Cycle)
        vbox3.addWidget(self.X)
        vbox3.addWidget(self.Y)
        vbox3.addWidget(self.Z)
        vbox4.addWidget(self.table)
        hbox5.addWidget(self.SaveExcel_button)
        hbox5.addWidget(self.ResetTable_button)
        vbox4.addLayout(hbox5)
        hbox4.addLayout(vbox3)
        hbox4.addLayout(vbox4)
        #hbox4.addWidget(self.Alarm)


        vbox2.addLayout(hbox3)
        vbox2.addWidget(self.canvas)  # h2
        vbox2.addLayout(hbox4)
        hbox.addLayout(vbox2)
        vbox.addLayout(hbox)
        #self.setLayout(vbox)


        self.setLayout(vbox)

        #############################################################
        # self.btn = QPushButton('start cam', self)
        # self.btn.setCheckable(True)
        # self.btn.clicked.connect(self.onoffCam)
        # vbox.addWidget(self.btn)
        #############################################################

        # video area

        # self.frm = QLabel(self)
        # self.frm.setFrameShape(QFrame.Panel)
        # self.frm.resize(640,480)
        #
        # vbox = QHBoxLayout()
        # vbox.addLayout(vbox)
        # vbox.addWidget(self.frm,0)
        # #self.setFixedSize(size)
        # self.move(100, 100)
        # self.setWindowTitle('OpenCV + PyQt5')
        # self.show()

        #############################################################

        self.x3 = np.arange(500)
        self.y3 = np.ones(500, dtype=np.float) * np.nan
        self.line, = self.canvas.axes.plot(self.x3, self.y3, animated=True,color='green', label="x",lw=0.5)

        self.x2 = np.arange(500)
        self.y2 = np.ones(500, dtype=np.float) * np.nan
        self.line2, = self.canvas.axes.plot(self.x2, self.y2, animated=True, color='red', label="y", lw=0.5)

        self.x = np.arange(500)
        self.y = np.ones(500, dtype=np.float) * np.nan
        self.line3, = self.canvas.axes.plot(self.x, self.y, animated=True,  label="z", lw=0.5)
        self.canvas.axes.legend(loc="upper left")


    ###################################################################################

    def onoffCam(self, e):
        if self.btn.isChecked():
            self.btn.setText('stop cam')
            self.video.URL(url=Rtsp)
            self.video.startCam()
        else:
            self.btn.setText('start cam')
            self.video.stopCam()

    def recvImage(self, img):
        self.frm.setPixmap(QPixmap.fromImage(img))

    ###################################################################################

    def update(self,num,y,y2,y3,line1,line2,line3):
        #여기 라인 x,y,z로 바꾸어주면 끝
        global x_array
        global y_array
        global z_array
        #global Filenumber
        global array
        global Max_Value
        global Sensitivity_Value
        global Line
        global Initial_value
        global Initial_x, Initial_y, Initial_z, x_value, y_value , z_value, count, t1_x, t1_y, t1_z, t2_x, t2_y, t2_z, limit, CheckPoint_X,\
            CheckPoint_Y,CheckPoint_Z,CycleX_count,CycleY_count,CycleZ_count,Scale_count,Scale_value,table_Count,FixXcycle,FixYcycle,FixZcycle
        if array == 0 :
            x_array = []
            y_array = []
            z_array = []
            # filename = 'C:/Users/Ahw/PycharmProjects/EarthProject/Data/' + 'data_' + str(
            #     Filenumber) + '.txt'  # 파일 이름 따라가기
            # filename = 'D:/CallFwCgi_160328/CallFwCgi_160328/' + 'data_' + str(
            #     Filenumber) + '.txt'  # 파일 이름 따라가기
            #filename = 'D:/CallFwCgi_160328/CallFwCgi_160328/' + 'data.txt'
            filename = 'data.txt'

            #print(filename)

            try:
                r = open(filename, mode='rt', encoding='utf-8')  # 파일 열어서 읽기
                #print(path)
                k = r.read()
                #print(k)
                t = k.split(' ')  # 파일 열어서 스페이스바로 리스트 나누기
                r.close()
                os.remove(filename)
                #print(t)
            except:
                # Filenumber += 1
                # if Filenumber >= 20:
                #     Filenumber = 0
                #print('ttttttttttt')
                return [self.line, self.line2, self.line3]
                # print(type(k))
            #print(t)
            i = 0
            while i < 30:  # 열은 파일 x,y,z로 나누기 현재 data 개수가 3이기에 3으로 나눔
                try:
                    z_array.append(int(t[i],16))
                except:
                    print(' -----------------HERE Z---------------- ')
                    return [self.line, self.line2, self.line3]
                #print(i)
                try:
                    x_array.append(int(t[i + 1],16))
                except:
                    print(' -----------------HERE X---------------- ')
                    return [self.line, self.line2, self.line3]
                try:
                    y_array.append(int(t[i + 2],16))
                except:
                    print(' -----------------HERE Y---------------- ')
                    return [self.line, self.line2, self.line3]
                i = i + 3                # print(x_array)
                # print(y_array)
                # print(z_array)
            # Filenumber = Filenumber + 1
            # if Filenumber >= 20:
            #     Filenumber = 0
        if Initial_value == 0:
            Initial_z = int(z_array[array])
            Initial_y = int(y_array[array])
            Initial_x = int(x_array[array])
            Initial_value = 1
        x_value = int(x_array[array])
        y_value = int(y_array[array])
        z_value = int(z_array[array])
        if x_value < Initial_x-127:
            x_value = 255 + x_value
        if y_value < Initial_y-127:
            y_value = 255 + y_value
        if z_value < Initial_z-127:
            z_value = 255 + z_value
        #print(y)
        # if int(y) >= 13 :
        #     #y=y-2569999999i
        #     y=float("%0.1f" % float(y-Initial_z))
        y = float("%0.2f" % float((x_value - Initial_x)*2/127))

        # if int(y2) >= 13 :
        #     #y2 = y2 - 256
        #     y2=float("%0.1f" % float(y2-Initial_y))
        # print(y2)
        y2 = float("%0.2f" % float((y_value - Initial_y)*2/127))

        # if int(y3) > 13 :
        #     #y3 = y3 - 256
        #     y3=float("%0.1f" % float(y3-Initial_x))
        #     #print(y3)
        y3 = float("%0.2f" % float((z_value - Initial_z)*2/127))

        ############주기찾기#############
        if CheckPoint_X == 0 :
            FixXcycle = '시작'
            if (y > t1_x) and ( y > t2_x) and ( y > limit ):
                CheckPoint_X = 1
            # if (y2 > t1_y) and ( y2 > t2_y) and ( y2 > limit ):
            #     limit2 = y2
            # if (y3 > t1_z) and ( y3 > t2_z ) and ( y3 > limit ):
            #     limit3 = y3
        elif CheckPoint_X == 1 :
            if (y > t1_x) and ( y > t2_x) and ( y > limit ):
                CheckPoint_X = 2
            # if (y2 > t1_y) and ( y2 > t2_y) and ( y2 > limit ):
            #     limit2 = y2
            # if (y3 > t1_z) and ( y3 > t2_z ) and ( y3 > limit ):
            #     limit3 = y3
        elif CheckPoint_X == 2 :
            Xcycle = float("%0.2f" % (CycleX_count * 0.1))
            Xcycle_Hz = str(int(1 / Xcycle)) + "Hz  "
            FixXcycle = str((Xcycle_Hz))
            self.X.setText('    X:  ' + str(Xcycle))
            CheckPoint_X = 1
            CycleX_count = 0

        if CheckPoint_Y == 0 :
            FixYcycle = '시작'
            if (y2 > t1_y) and ( y2 > t2_y) and ( y2 > limit ):
                CheckPoint_Y =1
            # if (y3 > t1_z) and ( y3 > t2_z ) and ( y3 > limit ):
            #     limit3 = y3
        elif CheckPoint_Y == 1 :
            if (y2 > t1_y) and ( y2 > t2_y) and ( y2 > limit ):
                CheckPoint_Y =2
            # if (y3 > t1_z) and ( y3 > t2_z ) and ( y3 > limit ):
            #     limit3 = y3
        elif CheckPoint_Y == 2 :
            Ycycle = float("%0.2f" % (CycleY_count * 0.1))
            Ycycle_Hz = str(int(1 / Ycycle)) + "Hz  "

            FixYcycle = str(Ycycle_Hz)
            self.Y.setText('    Y:  ' + str(Ycycle))
            CheckPoint_Y = 1
            CycleY_count = 0

        if CheckPoint_Z == 0 :
            FixZcycle = '시작'
            if (y3 > t1_z) and ( y3 > t2_z ) and ( y3 > limit ):
                CheckPoint_Z = 1
        elif CheckPoint_Z == 1 :
            if (y3 > t1_z) and ( y3 > t2_z ) and ( y3 > limit ):
                CheckPoint_Z = 2
        elif CheckPoint_Z == 2 :
            Zcycle = float("%0.2f" % (CycleZ_count * 0.1))
            Zcycle_Hz = str(int(1 / Zcycle)) + "Hz"
            FixZcycle = str(Zcycle_Hz)
            self.Z.setText('    Z:  ' + str(Zcycle))
            CheckPoint_Z = 1
            CycleZ_count = 0

        if ((y-t1_x<=0.02)or(t1_x-t2_x<=0.02)) \
                and ((y2-t1_y<=0.02)or(t1_y-t2_y<=0.02)) \
                and ((y3-t1_z<=0.02)or(t1_z-t2_z<=0.02))  :

            # x_value = int(x_array[array])
            # y_value = int(y_array[array])
            # z_value = int(z_array[array])
            # if x_value < Initial_x - 127:
            #     x_value = 255 + x_value
            # if y_value < Initial_y - 127:
            #     y_value = 255 + y_value
            # if z_value < Initial_z - 127:
            #     z_value = 255 + z_value
            # t = int(x_array[array])-Initial_x
            # t = t*0.5
            # Initial_z = int(z_array[array])-t
            # Initial_y = int(y_array[array])-t
            # Initial_x = int(x_array[array])-t

            Initial_z = int(z_array[array])
            Initial_y = int(y_array[array])
            Initial_x = int(x_array[array])
            if Initial_x < 127:
                Initial_x = 255 + Initial_x
            if Initial_y < 127:
                Initial_y = 255 + Initial_y
            if Initial_z < 127:
                Initial_z = 255 +Initial_z
            # if Initial_z < 12 :
            #     Initial_z = Initial_z + 26
            # if Initial_y < 5 :
            #     Initial_y = Initial_z + 26
            # if Initial_x < 5 :
            #     Initial_x = Initial_z + 26
            #print('k')

        old_y = self.line.get_ydata()
        new_y = np.r_[old_y[1:], y]
        self.line.set_ydata(new_y)

        old_y2 = self.line2.get_ydata()
        new_y2 = np.r_[old_y2[1:], y2]
        self.line2.set_ydata(new_y2)

        old_y3 = self.line3.get_ydata()
        new_y3 = np.r_[old_y3[1:], y3]
        self.line3.set_ydata(new_y3)

        if count == 2 :
            count = 0

        if count == 1:
            t2_x = y
            t2_y = y2
            t2_z = y3
            count = 2

        if count == 0:
            t1_x = y
            t1_y = y2
            t1_z = y3
            count = 1
        #########주기값#########


        if (abs(y) >= abs(y2)) and (abs(y) >= abs(y3)):
            Sensitivity_Value = abs(y)
            direction = "X - "
        elif (abs(y2) >= abs(y)) and (abs(y2) >= abs(y3)):
            Sensitivity_Value = abs(y2)
            direction = "Y - "
        else:
            Sensitivity_Value = abs(y3)
            direction = "Z - "
        if array == 4:
            self.sensitivity.setText('   Sensitivity: ' + str(Sensitivity_Value))
        # print(y)
        # print(y2)
        # print(y3)
        if (Max_Value < Sensitivity_Value):
            Max_Value = Sensitivity_Value
        self.Max.setText('   MAX: ' + str(Max_Value))

        #plottext = r'$\vec a _\max= '+str(y2)+'m/s^2$'

        ##############진도 찾기##################
        if Scale_value<Sensitivity_Value:
            Scale_value = Sensitivity_Value
            Fix_direction = direction
        if Scale_count == 50: ## 5초마다 실행

            if Scale_value <0.001 :
                Scale = '무감'
            elif Scale_value <=0.005 :
                Scale = '미진'
            elif Scale_value <=0.024 :
                Scale = '경진'
            elif Scale_value <=0.067 :
                Scale = '약진'
            elif Scale_value <=0.13 :
                Scale = '중진'
            elif Scale_value <=0.24 :
                Scale = '약 강진'
            elif Scale_value <=0.44 :
                Scale = '강 강진'
            elif Scale_value <=0.83 :
                Scale = '약 열진'
            elif Scale_value <=1.56 :
                Scale = '강 열진'
            elif Scale_value >1.56 :
                Scale = '격진'
            if Scale_value >= limit:
                # 표에 데이터 삽입
                now = datetime.datetime.now()
                nowDatetime = now.strftime('%m-%d %H:%M:%S')
                item1 = QTableWidgetItem(nowDatetime)
                item1.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(table_Count, 0, item1)

                item2 = QTableWidgetItem(str(Scale))
                item2.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(table_Count, 1, item2)

                item3 = QTableWidgetItem('X:'+FixXcycle+', Y:'+FixYcycle+', Z:'+FixZcycle)
                item3.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(table_Count, 2, item3)

                item4 = QTableWidgetItem(Fix_direction+str(Scale_value)+' g')
                item4.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(table_Count, 3, item4)
                #Screenshot_thread('EarthQuake')
                table_Count += 1
                index = self.table.model().index(table_Count,0)
                self.table.scrollTo(index)
                if table_Count > 999:
                    table_Count = 0
                    self.WriteCsv()
                    self.ResetTable()
                ##############################

            self.Scale.setText('  Scale:  ' + Scale)
            #print('k')
            Scale_count = 0
            Scale_value = 0
        Scale_count+=1
        array+=1
        if array > 9 :
            array = 0

        if CheckPoint_X == 1 :
            CycleX_count+=1
        if CycleX_count > 600:
            CycleX_count = 0
            CheckPoint_X = 0
            self.X.setText('    X:      ')
        if CheckPoint_Y == 1 :
            CycleY_count+=1
        if CycleY_count > 600:
            CycleY_count = 0
            CheckPoint_Y = 0
            self.Y.setText('    Y:      ')
        if CheckPoint_Z == 1 :
            CycleZ_count+=1
        if CycleZ_count > 600:
            CycleZ_count = 0
            CheckPoint_Z = 0
            self.Z.setText('    Z:      ')

        return [self.line, self.line2, self.line3]

    def on_start(self):
        self.ani = animation.FuncAnimation(self.canvas.figure, self.update, fargs=[self.y, self.y2,self.y3, self.line, self.line2, self.line3],blit=True, interval=25)

    def on_stop(self):
        self.ani._stop()

    def Limit(self):
        global limit,CheckPoint_X,CheckPoint_Y,CheckPoint_Z,CycleX_count,CycleY_count,CycleZ_count
        CheckPoint_X = 0
        CheckPoint_Y = 0
        CheckPoint_Z = 0
        CycleX_count = 0
        CycleY_count = 0
        CycleZ_count = 0
        self.X.setText('    X:      ')
        self.Y.setText('    Y:      ')
        self.Z.setText('    Z:      ')
        if self.Detect_Value.currentIndex() == 0 :
            limit = 0.005
        elif self.Detect_Value.currentIndex() == 1 :
            limit = 0.024
        elif self.Detect_Value.currentIndex() == 2 :
            limit = 0.067
        elif self.Detect_Value.currentIndex() == 3 :
            limit = 0.13
        elif self.Detect_Value.currentIndex() == 4 :
            limit = 0.24
        elif self.Detect_Value.currentIndex() == 5 :
            limit = 0.44
        elif self.Detect_Value.currentIndex() == 6 :
            limit = 0.83
        elif self.Detect_Value.currentIndex() == 7 :
            limit = 1.56


    def ResetTable(self):
        global table_Count
        self.table.clear()
        self.table.setHorizontalHeaderLabels(['시간', '진도', '주기', '크기'])
        table_Count = 0


    def WriteCsv(self):
        Folder = "./ExcelData"
        if not os.path.isdir(Folder):
            os.mkdir(Folder)
        now = datetime.datetime.now()
        Nowtime = now.strftime('%m%d_%H_%M_%S')
        path = "./ExcelData/"+"Table_"+Nowtime+".csv"
        print("saving", path)

        f = open(path, 'w', newline='')

        writer = csv.writer(f)
        for row in range(self.table.rowCount()):
            rowdata = []
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item is not None:
                    rowdata.append(item.text())
                else:
                    rowdata.append('')
            writer.writerow(rowdata)
        self.isChanged = False
        f.close()
        #self.setCurrentFile(path)
#####################################################################################


#####################################################################################
if __name__ == "__main__":
    # t=threading.Thread(target=AnimationWidget.MQ)
    # t.start()
    qApp = QApplication(sys.argv)
    aw = AnimationWidget()
    aw.show()
    sys.exit(qApp.exec_())