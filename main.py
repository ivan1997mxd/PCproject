import os
import sys
import time
import pymysql
import cv2
import math
from PyQt5 import QtCore, QtWidgets, QtGui, QtMultimedia
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit, QInputDialog, QMessageBox
from live import VideoBox
from view.login import *
from view.mainwindow2 import Ui_MainWindow
import pyttsx3

current_dir = os.path.dirname(os.path.abspath(__file__))
music_dir = current_dir + r'\music'

music_files = os.listdir(music_dir)


class LoginWindow(QMainWindow, Ui_login):
    def __init__(self):
        super().__init__()

        self.connection = pymysql.connect("localhost", "root", "root", "login")
        self.myCursor = self.connection.cursor()
        self.login = MainWindow()
        self.setupUi(self)
        self.loginBtn.clicked.connect(self.login_click)
        print("Login window opened!")

    def login_click(self, event):
        name = self.username.text()
        pwd = self.password.text()
        sql = "SELECT * FROM users where username= %s and password= %s"
        result = self.myCursor.execute(sql, [name, pwd])
        if name != "" and pwd != "":
            if result:
                QMessageBox.information(self, "恭喜," + name, "登陆成功", QMessageBox.Ok)
                self.hide()
                self.login.show()
            else:
                QMessageBox.information(self, "错误", "用户名或密码错误", QMessageBox.Ok)
                self.username.setText("")
                self.password.setText("")
        else:
            QMessageBox.information(self, "错误", "用户名和密码不能为空", QMessageBox.Ok)


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

        self.browserLayout = QtWidgets.QGridLayout(self.browserWindow)
        self.browserLayout.setObjectName("BrowserLayout")
        self.browser = QWebEngineView()
        url = 'https://www.baidu.com/'  # http://192.168.0.20:4200
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(url))
        self.browserLayout.addWidget(self.browser, 1, 1, 1, 1)

        # # 树莓派
        # self.browserLayout = QtWidgets.QGridLayout(self.browserWindow)
        # self.browserLayout.setObjectName("BrowserLayout")
        # self.browser = QWebView()
        # url = 'http://192.168.0.20:4200'
        # # 指定打开界面的 URL
        # self.browser.setUrl(QUrl(url))
        # self.browserLayout.addWidget(self.browser, 1, 1, 1, 1)

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
            self.input.setText("")
            engine = pyttsx3.init()
            engine.setProperty("voice",
                               "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0")
            engine.say(content)
            engine.runAndWait()

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
