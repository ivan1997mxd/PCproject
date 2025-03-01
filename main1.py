import os
import numpy as np
from PIL import Image
import sys
import sip
import time
import pymysql
import cv2
import math
import socket
import threading
import pyttsx3.drivers
from PyQt5.QtNetwork import *
from PyQt5.QtWebChannel import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebKit import *
from PyQt5.QtPrintSupport import *
# from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWidgets import *
from live import VideoBox
from view.login import *
from view.setting import *
from view.signup import *
from view.mainwindowUI import Ui_MainWindow
from aip import AipSpeech
import pyttsx3
import requests

import RPi.GPIO as GPIO

Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Relay_Ch1, GPIO.OUT)
GPIO.setup(Relay_Ch2, GPIO.OUT)
GPIO.setup(Relay_Ch3, GPIO.OUT)

APP_ID = '16437607'
API_KEY = 'l6Ib6bauea3tdAQeEkoHF22Q'
SECRET_KEY = 'yvmk3rWwKpjzYcBaF0oCkhGFHvn6GsMT'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


class checkStatus(threading.Thread):
    def __init__(self):
        super(checkStatus, self).__init__()

    def run(self):
        connectFile = os.popen('lsusb')
        list = connectFile.readlines()
        for i in range(len(list)):
            print(list[i])
            if list[i].find('printer1') != -1:
                self.printer1 = "条码打印机已连接"
            if list[i].find('printer2') != -1:
                self.printer2 = "发票打印机已连接"
            if list[i].find('Webcam') != -1:
                self.camera = "摄像头已连接"
                mainWindow.cameraStatus.setText("在线")
                print("online")
            else:
                mainWindow.cameraStatus.setText("离线")
            if list[i].find('gun') != -1:
                self.gun = "扫描枪已连接"
                mainWindow.gunStatus.setText("在线")
            else:
                mainWindow.gunStatus.setText("离线")
            if list[i].find('scale') != -1:
                self.scale = "电子秤已连接"
                mainWindow.scaleStatus.setText("在线")
            else:
                mainWindow.scaleStatus.setText("离线")


class speakWord(threading.Thread):
    def __init__(self, content):
        super(speakWord, self).__init__()
        self.content = content

    def run(self):
        result = client.synthesis(self.content, options={'vol': 5})
        if not isinstance(result, dict):
            with open('auido.mp3', 'wb') as f:
                f.write(result)
        os.system('omxplayer auido.mp3')


class lightCheck(threading.Thread):
    def __init__(self):
        super(lightCheck, self).__init__()

    def run(self):
        try:
            GPIO.output(Relay_Ch1, GPIO.LOW)
            print("Channel 1:The Common Contact is access to the Normal Open Contact!")
            time.sleep(0.5)

            GPIO.output(Relay_Ch1, GPIO.HIGH)
            print("Channel 1:The Common Contact is access to the Normal Closed Contact!\n")
            time.sleep(0.5)

            # Control the Channel 2
            GPIO.output(Relay_Ch2, GPIO.LOW)
            print("Channel 2:The Common Contact is access to the Normal Open Contact!")
            time.sleep(0.5)

            GPIO.output(Relay_Ch2, GPIO.HIGH)
            print("Channel 2:The Common Contact is access to the Normal Closed Contact!\n")
            time.sleep(0.5)

            # Control the Channel 3
            GPIO.output(Relay_Ch3, GPIO.LOW)
            print("Channel 3:The Common Contact is access to the Normal Open Contact!")
            time.sleep(0.5)

            GPIO.output(Relay_Ch3, GPIO.HIGH)
            print("Channel 3:The Common Contact is access to the Normal Closed Contact!\n")
            time.sleep(0.5)
            return True
        except Exception as e:
            print(e)
            return False


class SignWindow(QMainWindow, Ui_signup):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.photoShow = ""
        self.connection = pymysql.connect("localhost", "root", "root", "login")
        self.myCursor = self.connection.cursor()

        self.signBtn.clicked.connect(self.signup)
        self.pickBtn.clicked.connect(self.pickPhoto)
        self.shotBtn.clicked.connect(self.shotPhoto)

    def pickPhoto(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.photo.width(), self.photo.height())
        self.photo.setPixmap(jpg)
        self.photoShow = imgName

    def shotPhoto(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            k = cv2.waitKey(1)
            if k == ord('s'):
                cv2.imwrite('new.jpg', frame)
                break
            cv2.imshow("capture", frame)
        cap.release()
        cv2.destroyAllWindows()
        jpg = QtGui.QPixmap("new.jpg").scaled(self.photo.width(), self.photo.height())
        self.photo.setPixmap(jpg)
        self.photoShow = "new.jpg"

    def signup(self):
        name = self.username.text()
        pwd = self.password.text()
        age = self.ageBox.value()
        job = self.jobBox.currentText()
        fp = open(self.photoShow, "rb")
        photo = fp.read()
        print(name, pwd, age, job)
        sql = "INSERT INTO users(user_name, user_pwd, user_age, user_job, user_photo) VALUES (%s,%s,%s,%s,%s)"
        if name != "" and pwd != "":
            result = self.myCursor.execute(sql, [name, pwd, age, job, photo])
            self.connection.commit()
            if result:
                QMessageBox.information(self, "恭喜," + name, "用户创建成功", QMessageBox.Ok)
                replay = QMessageBox.information(self, "欢迎用户" + name, "请问是否要开始人脸注册", QMessageBox.Yes | QMessageBox.No)
                if replay == QMessageBox.Yes:
                    self.face_register(name, pwd)
                else:
                    self.myCursor.close()
                    self.connection.close()
                    self.close()
                    window.show()
        else:
            QMessageBox.information(self, "错误", "用户名和密码不能为空", QMessageBox.Ok)

    def face_register(self, name, pwd):
        cam = cv2.VideoCapture(0)
        cam.set(3, 640)  # set video width
        cam.set(4, 480)  # set video height

        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # For each person, enter one numeric face id
        sql = "SELECT user_id FROM users where user_name= %s and user_pwd= %s"
        self.myCursor.execute(sql, [name, pwd])
        result = self.myCursor.fetchone()
        userID = result[0]
        print(userID)
        face_id = userID
        self.myCursor.close()
        self.connection.close()

        print("\n [INFO] Initializing face capture. Look the camera and wait ...")
        # Initialize individual sampling face count
        count = 0

        while True:

            ret, img = cam.read()
            img = cv2.flip(img, 1)  # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1

                # Save the captured image into the datasets folder
                cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

                cv2.imshow('image', img)

            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 30:  # Take 30 face sample and stop video
                break

        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()
        QMessageBox.information(self, "人脸拍摄完毕", "一共拍摄：" + str(count) + "张", QMessageBox.Ok)
        self.face_traning()

    def face_traning(self):
        path = 'dataset'

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

        def getImagesAndLabels(path):

            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            ids = []

            for imagePath in imagePaths:

                PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
                img_numpy = np.array(PIL_img, 'uint8')

                id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = detector.detectMultiScale(img_numpy)

                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y + h, x:x + w])
                    ids.append(id)

            return faceSamples, ids

        print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        QMessageBox.information(self, "处理中", "正在加载图片请稍后", QMessageBox.Ok)
        faces, ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.write('trainer/trainer.yml')  # recognizer.save() worked on Mac, but not on Pi

        # Print the numer of faces trained and end program
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
        QMessageBox.information(self, "处理完毕", "完成人脸注册", QMessageBox.Ok)
        self.close()
        window.show()


class LoginWindow(QMainWindow, Ui_login):
    def __init__(self):
        super().__init__()

        self.connection = pymysql.connect("localhost", "root", "root", "login")
        self.myCursor = self.connection.cursor()
        self.signWindow = SignWindow()
        self.setupUi(self)
        self.ID = 0
        self.printer1 = "条码打印机未连接"
        self.printer2 = "发票打印机未连接"
        self.camera = "摄像头未连接"
        self.gun = "扫描枪未连接"
        self.scale = "电子秤未连接"
        self.loginBtn.clicked.connect(self.login_click)
        self.faceBtn.clicked.connect(self.face_recognition)
        self.faceRegister.clicked.connect(self.register)
        print("Login window opened!")

    def register(self):
        self.signWindow.show()
        self.close()

    def login_click(self):
        name = self.username.text()
        pwd = self.password.text()

        if name != "" and pwd != "":
            sql = "SELECT * FROM users where user_name= %s and user_pwd= %s"
            result = self.myCursor.execute(sql, [name, pwd])
            if result:
                self.ID = self.myCursor.fetchone()[0]
                QMessageBox.information(self, "恭喜," + name, "登陆成功", QMessageBox.Ok)
                self.loginDone(name)
            else:
                QMessageBox.information(self, "错误", "用户名或密码错误", QMessageBox.Ok)
                self.username.setText("")
                self.password.setText("")
        else:
            QMessageBox.information(self, "错误", "用户名和密码不能为空", QMessageBox.Ok)

    def checkDevice(self):
        connectFile = os.popen('lsusb')
        list = connectFile.readlines()
        for i in range(len(list)):
            print(list[i])
            if list[i].find('printer1') != -1:
                self.printer1 = "条码打印机已连接"
            if list[i].find('printer2') != -1:
                self.printer2 = "发票打印机已连接"
            if list[i].find('Webcam') != -1:
                self.camera = "摄像头已连接"
                mainWindow.cameraStatus.setText("在线")
                print("online")
            else:
                mainWindow.cameraStatus.setText("离线")
            if list[i].find('gun') != -1:
                self.gun = "扫描枪已连接"
                mainWindow.gunStatus.setText("在线")
            else:
                mainWindow.gunStatus.setText("离线")
            if list[i].find('scale') != -1:
                self.scale = "电子秤已连接"
                mainWindow.scaleStatus.setText("在线")
            else:
                mainWindow.scaleStatus.setText("离线")

    def loginDone(self, id):
        hostname = socket.gethostname()
        # engine = pyttsx3.init()
        # engine.setProperty("voice",
        # "zh+f2")
        self.checkDevice()
        status = self.printer1 + ',' + self.printer2 + ',' + self.camera + ',' + self.gun + ',' + self.scale
        content = id + ", 欢迎登录" + hostname + "号工作台，设备自检中，" + status
        print(content)
        speak = speakWord(content)
        speak.start()
        # self.myCursor.close()
        # self.connection.close()
        self.close()
        mainWindow.show()
        mainWindow.check()
        # engine.say(content)
        # engine.runAndWait()

    def face_recognition(self):

        result = True

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)

        font = cv2.FONT_HERSHEY_SIMPLEX

        sql = "SELECT user_name,user_id FROM login.users"
        self.myCursor.execute(sql)
        names = []
        ids = []
        allResult = self.myCursor.fetchall()
        for row in allResult:
            names.append(row[0])
            ids.append(row[1])
        print(names)
        print(ids)

        # names related to ids: example ==> Marcelo: id=1,  etc
        # names = ['None', 'Ivan', 'Paula', 'Ilza', 'Z', 'W']

        # iniciate id counter
        id = 0

        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
        cam.set(3, 640)  # set video widht
        cam.set(4, 480)  # set video height

        # Define min window size to be recognized as a face
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)

        while result:

            ret, img = cam.read()
            img = cv2.flip(img, 1)  # Flip vertically

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for (x, y, w, h) in faces:

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                # Check if confidence is less them 100 ==> "0" is perfect match
                if confidence < 100:
                    index = ids.index(id)
                    self.ID = id
                    id = names[index]
                    confidence = "  {0}%".format(round(100 - confidence))
                    reply = QMessageBox.information(self, "人脸识别成功,", "用户：" + id + ",请问是否要以此账号登录",
                                                    QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        result = False

                    else:
                        continue
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

            cv2.imshow('camera', img)

            k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break

        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()
        self.loginDone(id)


class SettingWindow(QWidget, Ui_setting):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connection = pymysql.connect("localhost", "root", "root", "login")
        self.myCursor = self.connection.cursor()
        self.check()

        self.print1 = QPrinter()
        self.print2 = QPrinter()
        self.print3 = QPrinter()
        self.tagSetting.clicked.connect(self.tag_click)
        self.reportSetting.clicked.connect(self.report_click)
        self.invoiceSetting.clicked.connect(self.invoice_click)
        self.save.clicked.connect(self.save_click)

    def check(self):
        hostname = socket.gethostname()
        sql = 'SELECT tag_printer, report_printer, invoice_printer FROM printer WHERE printer_PC=%s'
        result = self.myCursor.execute(sql, [hostname])
        if result:
            allPrinters = self.myCursor.fetchall()
            for row in allPrinters:
                self.tagEdit.setText(row[0])
                self.reportEdit.setText(row[1])
                self.invoiceEdit.setText(row[2])

    def save_click(self):
        tag_printer = self.print1.printerName()
        report_printer = self.print3.printerName()
        invoice_printer = self.print2.printerName()
        hostname = socket.gethostname()
        sql = 'SELECT * FROM printer WHERE printer_PC=%s'
        result = self.myCursor.execute(sql, [hostname])
        if result:
            sql1 = "UPDATE printer Set tag_printer=%s, report_printer=%s, invoice_printer=%s WHERE printer_PC=%s"
            self.myCursor.execute(sql1, [tag_printer, report_printer, invoice_printer, hostname])
            self.connection.commit()
        else:
            sql2 = "INSERT INTO printer(tag_printer, report_printer, invoice_printer, printer_PC) VALUES (%s, %s, %s, %s)"
            self.myCursor.execute(sql2, [tag_printer, report_printer, invoice_printer, hostname])
            self.connection.commit()

        self.close()

    def tag_click(self):
        # 实例化打印图像对象
        printer = QPrinter()
        # 打印窗口弹出
        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_():
            self.tagEdit.setText(printer.printerName())
            self.print1.setPrinterName(printer.printerName())
            printDialog.close()

    def invoice_click(self):
        # 实例化打印图像对象
        printer = QPrinter()
        # 打印窗口弹出
        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_():
            self.invoiceEdit.setText(printer.printerName())
            self.print2.setPrinterName(printer.printerName())
            printDialog.close()

    def report_click(self):
        # 实例化打印图像对象
        printer = QPrinter()
        # 打印窗口弹出
        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_():
            self.reportEdit.setText(printer.printerName())
            self.print3.setPrinterName(printer.printerName())
            printDialog.close()


class MainWindow(QMainWindow, Ui_MainWindow):
    toHtmlFinished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.videoWidget = VideoBox()
        self.setupUi(self)
        self.setting = SettingWindow()

        self.connection = pymysql.connect("localhost", "root", "root", "login")
        self.myCursor = self.connection.cursor()

        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.__flag_work = 0
        self.x = 0
        self.fileName = ""
        self.switch = True
        self.printer = QPrinter()

        # Windows
        # self.browserLayout = QtWidgets.QGridLayout(self.browserWindow)
        # self.browserLayout.setObjectName("BrowserLayout")
        # self.browser = QWebEngineView()
        # self.url = 'https://www.baidu.com/'#'http://rtxtst.domain.cn:4200'  # http://192.168.0.20:4200
        # # 指定打开界面的 URL
        # self.browser.setUrl(QUrl(self.url))
        # self.browserLayout.addWidget(self.browser, 1, 1, 1, 1)
        # self.engine = pyttsx3.init()
        # self.engine.setProperty("voice",
        # "zh+f2")

        # 树莓派
        self.browserLayout = QtWidgets.QGridLayout(self.browserWindow)
        self.browserLayout.setObjectName("BrowserLayout")
        self.browser = QWebView()
        self.url = 'http://rtxwms.domain.com:4200'
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(self.url))
        self.browserLayout.addWidget(self.browser, 1, 1, 1, 1)

        self.yellowlight.clicked.connect(self.setYellow)
        self.greenlight.clicked.connect(self.setGreen)
        self.redlight.clicked.connect(self.setRed)
        self.live.clicked.connect(self.setLive)
        self.timer_camera.timeout.connect(self.show_camera)
        self.start.clicked.connect(self.setRecord)
        self.stop.clicked.connect(self.setStop)
        self.open.clicked.connect(self.setOpen)
        self.send.clicked.connect(self.setSend)
        self.tsmi_homePage.triggered.connect(self.MainPage)
        self.tsmiPrinter.triggered.connect(self.Printer)
        self.tsmiPageset.triggered.connect(self.PageSet)
        self.tsmiReceiptLabel.triggered.connect(self.Receipt)
        self.tsmiB2Clist.triggered.connect(self.B2CList)
        self.tsmiB2BRePrint.triggered.connect(self.B2BReprint)
        self.actionforward.triggered.connect(self.browser.forward)
        self.actionbackward.triggered.connect(self.browser.back)
        self.logout.clicked.connect(self.logout_click)

    def printerTest_clicked(self):
        printDialog = QPrintDialog(self.printer, self)
        if printDialog.exec_():
            name = self.printer.printerName()
            self.statusbar.showMessage(name)
            self.printerStatus.setText(name[0:20])
            printDialog.close()

    def logout_click(self):
        self.close()
        window.show()

    def check(self):
        print("Main window opened!")

        id = window.ID
        sql = "SELECT * FROM users where user_id=%s"
        self.myCursor.execute(sql, [id])
        infoList = self.myCursor.fetchone()
        self.name.setText(infoList[1])
        self.age.setText(str(infoList[3]))
        self.job.setText(infoList[4])
        self.loginTime.setText(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

        stuffPhoto = open("stuff.jpg", "wb")
        stuffPhoto.write(infoList[5])
        stuffPhoto.close()
        jpg = QtGui.QPixmap("stuff.jpg").scaled(self.stuffPhoto.width(), self.stuffPhoto.height())
        self.stuffPhoto.setPixmap(jpg)
        light = lightCheck()
        light.start()
        device = checkStatus()
        device.start()

    def isConnect(self):
        try:
            html = requests.get("https://www.baidu.com/", timeout=2)
        except:
            self.internetStatus.setText("离线")
        self.internetStatus.setText("在线")

    # def lightCheck(self):
    #     try:
    #         GPIO.output(Relay_Ch1, GPIO.LOW)
    #         print("Channel 1:The Common Contact is access to the Normal Open Contact!")
    #         time.sleep(0.5)
    #
    #         GPIO.output(Relay_Ch1, GPIO.HIGH)
    #         print("Channel 1:The Common Contact is access to the Normal Closed Contact!\n")
    #         time.sleep(0.5)
    #
    #         # Control the Channel 2
    #         GPIO.output(Relay_Ch2, GPIO.LOW)
    #         print("Channel 2:The Common Contact is access to the Normal Open Contact!")
    #         time.sleep(0.5)
    #
    #         GPIO.output(Relay_Ch2, GPIO.HIGH)
    #         print("Channel 2:The Common Contact is access to the Normal Closed Contact!\n")
    #         time.sleep(0.5)
    #
    #         # Control the Channel 3
    #         GPIO.output(Relay_Ch3, GPIO.LOW)
    #         print("Channel 3:The Common Contact is access to the Normal Open Contact!")
    #         time.sleep(0.5)
    #
    #         GPIO.output(Relay_Ch3, GPIO.HIGH)
    #         print("Channel 3:The Common Contact is access to the Normal Closed Contact!\n")
    #         time.sleep(0.5)
    #         self.lightStatus.setText("在线")
    #     except Exception as e:
    #         print(e)
    #         self.lightStatus.setText("离线")
    #

    def Receipt(self):
        file_url = "http://rtxwms.domain.com:8580/birt/output?__report=report/Rtx_B2Byxhbq_Tag_New.rptdesign&__showtitle=false&__asattachment=false&__offsetMin=0&__locale=zh&orderkey=0000026675&LPNid=X000000647&__format=html&&__pageoverflow=0&__overwrite=false"
        self.browser.setUrl(QUrl(file_url))

    def B2CList(self):
        file_url = "http://rtxwms.domain.com:8580/birt/output?__report=report/Rtx_B2Byxhbq_Tag_New.rptdesign&__showtitle=false&__asattachment=false&__offsetMin=0&__locale=zh&orderkey=0000026675&LPNid=X000000647&__format=html&&__pageoverflow=0&__overwrite=false"
        self.browser.setUrl(QUrl(file_url))

    def B2BReprint(self):
        file_url = "http://rtxwms.domain.com:8580/birt/output?__report=report/Rtx_B2Byxhbq_Tag_New.rptdesign&__showtitle=false&__asattachment=false&__offsetMin=0&__locale=zh&orderkey=0000026675&LPNid=X000000647&__format=html&&__pageoverflow=0&__overwrite=false"
        self.browser.setUrl(QUrl(file_url))

    def PageSet(self):
        # self.browser.page().print(self.printer, self.callback)
        self.printer.setOutputFormat(QPrinter.PdfFormat)
        self.printer.setOutputFileName('a.pdf')
        self.browser.print(self.printer)
        os.system("xdg-open a.pdf")

    def callback(is_ok):
        if is_ok:
            print('printing finished')
        else:
            print('printing error')

    def Printer(self):
        self.setting.show()

    def MainPage(self):
        print("clicked!")
        self.browser.load(QUrl(self.url))

    def setSend(self):
        content = self.input.text()
        if content.strip():
            self.input.setText("")
            speak = speakWord(content)
            speak.start()
            # self.engine.say(content)
            # self.engine.runAndWait()

        else:
            self.statusbar.showMessage("输入为空")

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
                cv2.putText(frame, self.fileName, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (55, 255, 155), 2)
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
            GPIO.output(Relay_Ch1, GPIO.LOW)
        else:
            GPIO.output(Relay_Ch1, GPIO.HIGH)

    def setRed(self):
        if self.redlight.isChecked():
            GPIO.output(Relay_Ch3, GPIO.LOW)
        else:
            GPIO.output(Relay_Ch3, GPIO.HIGH)

    def setGreen(self):
        if self.greenlight.isChecked():
            GPIO.output(Relay_Ch2, GPIO.LOW)
        else:
            GPIO.output(Relay_Ch2, GPIO.HIGH)

    # class Thread(QThread):
    #     show_signal = pyqtSignal(QImage)
    #     def __init__(self, file_name, browser):
    #         QThread.__init__(self)
    #         self.video_name = file_name
    #         self.browser = browser
    #
    #     def run(self):

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '系统',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            # GPIO.output(Relay_Ch2, GPIO.HIGH)
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    mainWindow = MainWindow()
    sys.exit(app.exec_())
