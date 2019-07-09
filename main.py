import os
import random
import sys
import time

import cv2
import math
from PyQt5 import QtCore, QtWidgets, QtGui, QtMultimedia
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit, QInputDialog
from PyQt5.QtMultimedia import *
from live import VideoBox
from login import Ui_Form
from view.mainwindow2 import Ui_MainWindow
from aip import AipSpeech
import pyttsx3

current_dir = os.path.dirname(os.path.abspath(__file__))
music_dir = current_dir + r'\music'

music_files = os.listdir(music_dir)


class LoginWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.login = MainWindow()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login_click)
        print("Login window opened!")

    def login_click(self):
        self.hide()
        self.login.show()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.videoWidget = VideoBox()
        self.setupUi(self)

        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.__flag_work = 0
        self.x = 0
        self.fileName = ""
        self.switch = True
        self.player = QtMultimedia.QMediaPlayer()

        self.yellowlight.clicked.connect(self.setYellow)
        self.greenlight.clicked.connect(self.setGreen)
        self.redlight.clicked.connect(self.setRed)
        self.live.clicked.connect(self.setLive)
        self.timer_camera.timeout.connect(self.show_camera)
        self.start.clicked.connect(self.setRecord)
        self.stop.clicked.connect(self.setStop)
        self.open.clicked.connect(self.setOpen)
        self.send.clicked.connect(self.setSend)
        print("Main window opened!")

    def setSend(self):
        content = self.input.text()
        if content.strip():
            self.output.append(content)
            engine = pyttsx3.init()
            engine.setProperty("voice",
                               "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0")
            engine.say(content)
            engine.runAndWait()
            self.input.setText("")
        else:
            print("input is empty")

    def setStop(self):
        self.switch = False
        self.fileName = ""
        self.start.setText("开始录像")
        self.start.setEnabled(True)
        self.stop.setEnabled(False)

    def setOpen(self):
        file_, okPressed = QFileDialog.getOpenFileName(self,
                                                       "选取文件",
                                                       "",
                                                       "Video files(*.avi , *.mp4)")  # 设置文件扩展名过滤,注意用双分号间隔
        if okPressed and file_ != '':
            self.videoWidget.set_video(file_, VideoBox.VIDEO_TYPE_OFFLINE, False)
            self.videoWidget.show()

    def setRecord(self):
        value, okPressed = QInputDialog.getText(self, "输入标题", "请输入视频名称(只有英文):", QLineEdit.Normal, "myVideo.avi")
        if okPressed and value != '':
            self.fileName = value
            self.start.setEnabled(False)
            self.startRecord()

    def startRecord(self):
        # keep_process = True
        self.stop.setEnabled(True)
        self.start.setText(u"录像中")
        codec = cv2.VideoWriter_fourcc(*'MJPG')
        fps = 25.0  # 指定写入帧率为25
        frameSize = (640, 480)  # 指定窗口大小
        # # 创建 VideoWriter对象
        # now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        output = cv2.VideoWriter(self.fileName, codec, fps, frameSize)
        if not (((len(sys.argv) == 2) and (self.cap.open(str(sys.argv[1]))))
                or (self.cap.open(self.CAM_NUM))):
            print("ERROR：No video file specified or camera connected.")
            return -1

        while self.cap.isOpened():
            if self.switch:
                ret, frame = self.cap.read()

                start_t = cv2.getTickCount()
                output.write(frame)
                stop_t = ((cv2.getTickCount() - start_t) / cv2.getTickFrequency()) * 1000
                key = cv2.waitKey(max(2, 40 - int(math.ceil(stop_t)))) & 0xFF
                if key == ord('q'):
                    keep_processing = False
            else:
                print("Quit Process ")
                break
        # print("The display and video write tasks take {} ms".format(stop_t))

    def setLive(self):
        if not self.timer_camera.isActive():
            flag = self.cap.open(self.CAM_NUM)
            if not flag:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            # if msg==QtGui.QMessageBox.Cancel:
            #                     pass
            else:
                self.timer_camera.start(30)
                self.start.setEnabled(True)
                self.live.setText(u'关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.video.clear()
            self.start.setEnabled(False)
            self.stop.setEnabled(False)
            self.fileName = ""
            self.start.setText(u"开始录像")
            self.live.setText(u'打开相机')

    def show_camera(self):
        flag, self.image = self.cap.read()
        # face = self.face_detect.align(self.image)
        # if face:
        #     pass

        show = cv2.resize(self.image, (640, 480))
        s = time.asctime()
        cv2.putText(show, self.fileName + " " + s, (10, 50), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 2)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.video.setPixmap(QtGui.QPixmap.fromImage(showImage))
        # self.x += 1
        # self.label_move.move(self.x,100)

        # if self.x ==320:
        #     self.label_show_camera.raise_()

    def setYellow(self):
        if self.yellowlight.isChecked():
            switch3_on = "sudo /home/pi/RPi_Relay_Board/shell/Relay.sh CH2 ON"
            os.system(switch3_on)
        else:
            switch3_off = "sudo /home/pi/RPi_Relay_Board/shell/Relay.sh CH2 OFF"
            os.system(switch3_off)

    def setRed(self):
        if self.redlight.isChecked():
            switch2_on = "sudo /home/pi/RPi_Relay_Board/shell/Relay.sh CH3 ON"
            os.system(switch2_on)
        else:
            switch2_off = "sudo /home/pi/RPi_Relay_Board/shell/Relay.sh CH3 OFF"
            os.system(switch2_off)

    def setGreen(self):
        if self.greenlight.isChecked():
            switch1_on = "sudo /home/pi/RPi_Relay_Board/shell/Relay.sh CH1 ON"
            os.system(switch1_on)
        else:
            switch1_off = "sudo /home/pi/RPi_Relay_Board/shell/Relay.sh CH1 OFF"
            os.system(switch1_off)


# class Thread(QThread):
#     show_signal = pyqtSignal(QImage)
#     def __init__(self, file_name, browser):
#         QThread.__init__(self)
#         self.video_name = file_name
#         self.browser = browser
#
#     def run(self):


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
