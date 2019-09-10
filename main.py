# -*- coding: utf-8 -*-
import os
import threading

import numpy as np
from PIL import Image
from ftplib import *
import sys
import time
import pymysql
import cv2
import math
import socket
import pyttsx3.drivers
import pyttsx3.drivers.sapi5
import pythoncom
import requests
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtWebChannel import QWebChannel
from bs4 import BeautifulSoup
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWebEngineWidgets import *
# from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWidgets import *
from live import VideoBox
from view.login import *
from view.setting import *
from view.signup import *
from view.mainwindowUI import Ui_MainWindow
import cx_Oracle
import pyttsx3

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
BASE_DIR = os.path.dirname(__file__)
host = '47.101.60.18'
username = 'user'
password = 'root'
file = '1.txt'
port = 21

filePath = os.path.dirname(os.path.abspath(__file__))


class Worker(QThread):
    sinOut = pyqtSignal(str)  # 自定义信号，执行run()函数时，从相关线程发射此信号

    def __init__(self, url):
        super(Worker, self).__init__()
        self.working = True
        self.done = ""
        self.url = url

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        while self.working:
            response = requests.get(self.url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            number = soup.find("label", id="count").get_text()
            self.done = number.split('/')[1]
            # 发出信号
            print(self.done)
            self.sinOut.emit(self.done)
            # 线程休眠2秒
            self.sleep(2)


def ftpconnect(host, port, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)         #打开调试级别2，显示详细信息
    ftp.encoding = 'utf-8'  # 解决中文编码问题，默认是latin-1
    try:
        ftp.connect(host, port)  # 连接
        ftp.login(username, password)  # 登录，如果匿名登录则用空串代替即可
        print(ftp.getwelcome())  # 打印欢迎信息
    except(socket.error, socket.gaierror):  # ftp 连接错误
        print("ERROR: cannot connect [{}:{}]".format(host, port))
        return None
    except error_perm:  # 用户登录认证错误
        print("ERROR: user Authentication failed ")
        return None
    return ftp


def is_ftp_file(ftp_conn, ftp_path):
    try:
        if ftp_path in ftp_conn.nlst(os.path.dirname(ftp_path)):
            return True
        else:
            return False
    except error_perm:
        return False


def uploadfile(ftp, remotepath, localpath):
    """
    上传文件
    :param ftp:
    :param remotepath:
    :param localpath:
    :return:
    """
    bufsize = 1024
    fp = open(localpath, 'rb')
    res = ftp.storbinary('STOR ' + remotepath, fp, bufsize)  # 上传文件
    if res.find('226') != -1:
        print('upload file complete', remotepath)
    ftp.set_debuglevel(0)
    fp.close()


def ftp_theadpool(func, ftp, file_list):
    """
    通过线程池调用上传文件列表
    :param func:
    :param file_list:
    :return:
    """
    pool = ThreadPoolExecutor(6)
    for remotepath, localpath in file_list:
        pool.submit(func, ftp, remotepath, localpath)
    pool.shutdown()


class SignWindow(QMainWindow, Ui_signup):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.photoShow = ""
        self.connection = pymysql.connect("47.101.60.18", "root", "root", "login")
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
            result = self.myCursor.execute(sql, [name, pwd, age, job, pymysql.Binary(photo)])
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
        self.myCursor.close()
        self.connection.close()
        self.close()
        window.show()


class LoginWindow(QMainWindow, Ui_login):
    def __init__(self):
        super().__init__()

        self.connection = pymysql.connect("47.101.60.18", "root", "root", "login")
        self.myCursor = self.connection.cursor()
        self.signWindow = SignWindow()
        self.setupUi(self)
        self.ID = 0
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

    def getdevlist(self):
        devlist = []
        connectfile = os.popen('lsusb')
        list = connectfile.readlines()
        print(list)
        for i in range(len(list)):
            if list[i].find('\tdevice') != -1:
                temp = list[i].split('\t')
                devlist.append(temp[0])
        return devlist

    def loginDone(self, id):
        hostname = socket.gethostname()
        engine = pyttsx3.init()
        engine.setProperty("voice",
                           "zh")

        content = id + ", 欢迎登录" + hostname + "号工作台，设备自检中，信号灯工作正常,1号打印机未联机，2号打印机未联机，称重设备未联机，祝你工作愉快！"
        # self.myCursor.close()
        # self.connection.close()
        self.close()
        mainWindow.show()
        mainWindow.check()
        engine.say(content)
        engine.runAndWait()

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
                if confidence < 65:
                    index = ids.index(id)
                    self.ID = id
                    id = names[index]
                    confidence = "  {0}%".format(round(100 - confidence))
                    reply = QMessageBox.information(self, "人脸识别成功,", "用户：" + id + ",请问是否要以此账号登录",
                                                    QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        print(id, self.ID, confidence)
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
        if id != 0:
            self.loginDone(id)


class SettingWindow(QWidget, Ui_setting):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connection = pymysql.connect("47.101.60.18", "root", "root", "login")
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
        else:
            self.tagEdit.setText("")
            self.reportEdit.setText("")
            self.invoiceEdit.setText("")

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
        self.setWindowTitle("仓库管理系统")
        self.videoWidget = VideoBox()
        self.setupUi(self)
        self.setting = SettingWindow()

        self.connection = pymysql.connect("47.101.60.18", "root", "root", "login")
        self.myCursor = self.connection.cursor()
        # Oracle DB

        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = "http://192.168.1.29:8080/?action=stream?dummy=param.mjpg"
        self.__flag_work = 0
        self.x = 0
        self.subtitle = ""
        self.switch = True

        # Windows
        self.browserLayout = QtWidgets.QGridLayout(self.browserWindow)
        self.browserLayout.setObjectName("BrowserLayout")
        self.browser = QWebEngineView(self)
        self.url = 'http://rtxwms.domain.com:4200'
        self.browser.load(QUrl(self.url))
        self.browser.show()

        self.browserLayout.addWidget(self.browser, 1, 1, 1, 1)
        self.engine = pyttsx3.init()
        self.engine.setProperty("voice",
                                "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0")

        # 树莓派
        # self.browserLayout = QtWidgets.QGridLayout(self.browserWindow)
        # self.browserLayout.setObjectName("BrowserLayout")
        # self.browser = QWebView()
        # url = 'http://rtxtst.domain.cn:4200'
        # # 指定打开界面的 URL
        # self.browser.setUrl(QUrl(url))
        # self.browserLayout.addWidget(self.browser, 1, 1, 1, 1)
        self.printer = QPrinter()
        self.html = ""
        self.hostname = socket.gethostname()
        self.yellowlight.clicked.connect(self.setYellow)
        self.greenlight.clicked.connect(self.setGreen)
        self.redlight.clicked.connect(self.setRed)
        self.live.clicked.connect(self.setLive)
        self.timer_camera.timeout.connect(self.show_camera)
        # self.start.clicked.connect(self.setRecord)
        # self.stop.clicked.connect(self.setStop)
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
        self.ftp = ftpconnect(host, port, username, password)
        self.browser.urlChanged.connect(self.urlChange)
        self.startM.clicked.connect(self.StartMission)
        self.endM.clicked.connect(self.EndMission)
        self.endM.setEnabled(False)
        self.progressBar.setValue(0)
        self.MyUrl = ""
        self.total = 0
        self.done = 0

    def checkProcess(self, done):
        self.done = int(done)
        if self.done != 0:
            percent = (self.done // self.total) * 100
            print(percent)
            self.progressBar.setValue(percent)
            self.doneNum.setText(done)
            if self.done == self.total:
                self.thread.__del__()
                print("it is finished!")

    def EndMission(self):
        self.setStop()
        url = "http://rtxwms.domain.com:8580/birt/output?__report=report/Rtx_B2Byxhbq_Tag_New.rptdesign&__showtitle=false&__asattachment=false&__offsetMin=0&__locale=zh&orderkey=" + self.orderKey + "&LPNid=" + self.expressKey + "&__format=html&&__pageoverflow=0&__overwrite=false"
        # url = "http://rtxwms.domain.com:8580/birt/output?__report=report/Rtx_B2Byxhbq_Tag_New.rptdesign&__showtitle=false&__asattachment=false&__offsetMin=0&__locale=zh&orderkey=0000026675&LPNid=X000000647&__format=html&&__pageoverflow=0&__overwrite=false"
        printWindow.webview.load(QUrl(url))
        # printWindow.show()
        printWindow.webview.loadFinished.connect(self.printPage)
        self.startM.setEnabled(True)
        self.endM.setEnabled(False)
        self.startM.setText("开始任务")
        self.totoalNum.setText("未知")
        self.doneNum.setText("未知")
        self.orderkeyNum.setText("未知")
        self.expresskeyNum.setText("未知")
        self.progressBar.setValue(0)

    def printPage(self):
        printWindow.webview.page().print(self.printer, self.callBack)

    def StartMission(self):
        self.orderKey = self.browser.selectedText()
        if self.orderKey != "":
            self.progressBar.setValue(0)
            self.MyUrl = "http://rtxwms.domain.com:8180/rtxextend/MainOrderSerlet?whseid=wmwhse1&orderkey=" + self.orderKey + "&opeuser=" + self.name.text()
            response = requests.get(self.MyUrl)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            self.expressKey = soup.find("label", id="lbl_expresskey").get_text()
            self.orderKey = soup.find("label", id="lbl_orderkey").get_text()
            self.subtitle = self.name.text() + " " + self.table.text() + " " + self.orderKey + " " + self.expressKey
            number = soup.find("label", id="count").get_text()
            total = number.split('/')[2]
            done = number.split('/')[1]
            self.total = int(total)
            self.totoalNum.setText(total)
            self.doneNum.setText(done)
            self.expresskeyNum.setText(self.expressKey)
            self.orderkeyNum.setText(self.orderKey)
            self.endM.setEnabled(True)
            self.startM.setEnabled(False)
            self.startM.setText("任务进行中")
            print(self.subtitle)
            self.startRecord()
        else:
            QMessageBox.information(self, "消息", "请先选取订单号！", QMessageBox.Ok)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            print(self.browser.selectedText())

    def urlChange(self):
        pageUrl = self.browser.page().url().toString()
        print(pageUrl)

    # def PageCookie(self, result):
    #     print(result)

    #     self.browser.page().runJavaScript("document.getElementById('closecase').value='关箱吧';")
    #     html = requests.get(self.browser.url().toString())
    #     html.encoding = html.apparent_encoding
    #     soup = BeautifulSoup(html.text, 'html.parser')
    #     a = soup.prettify()
    #     print(a)

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
        self.table.setText(self.hostname)
        self.loginTime.setText(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

        stuffPhoto = open("stuff.jpg", "wb")
        stuffPhoto.write(infoList[5])
        stuffPhoto.close()
        jpg = QtGui.QPixmap("stuff.jpg").scaled(self.stuffPhoto.width(), self.stuffPhoto.height())
        self.stuffPhoto.setPixmap(jpg)
        self.printerStatus.setText(self.printer.printerName())
        self.setLive()

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
        page = self.browser.page()
        # # page.toHtml(self.callback)
        page.print(self.printer, self.callBack)
        # self.printer.setOutputFormat(QPrinter.PdfFormat)
        # self.printer.setOutputFileName('a.pdf')
        # self.browser.page().print(self.printer, self.callBack)
        # os.system("xdg-open a.pdf")

    def callBack(self, x):
        if x:
            print('printing ok ' + str(x))
            QMessageBox.information(self, "消息", "打印完成", QMessageBox.Ok)
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
            self.engine.say(content)
            self.engine.runAndWait()
        else:
            print("input is empty")

    def setStop(self):
        self.switch = False
        uploadfile(self.ftp, self.now, filePath + "\\" + self.now + '.avi')
        self.subtitle = ""

    def setOpen(self):
        file_, okPressed = QFileDialog.getOpenFileName(self,
                                                       "选取文件",
                                                       "",
                                                       "Video files(*.avi , *.mp4)")  # 设置文件扩展名过滤,注意用双分号间隔
        if okPressed and file_ != '':
            self.videoWidget.set_video(file_, VideoBox.VIDEO_TYPE_OFFLINE, False)
            self.videoWidget.show()

    # def setRecord(self):
    #     value, okPressed = QInputDialog.getText(self, "输入标题", "请输入视频名称(只有英文):", QLineEdit.Normal, "操作员 工作台 订单号 箱号 时间")
    #     if okPressed and value != '':
    #         self.fileName = value
    #         self.start.setEnabled(False)
    #         self.startRecord()

    def speakWord(self):
        self.engine.say("加油加油！已经工作了30秒了")
        self.engine.runAndWait()

    def startRecord(self):
        # keep_process = True
        self.statusbar.showMessage("正在录像中")
        codec = cv2.VideoWriter_fourcc(*'MJPG')
        fps = 25.0  # 指定写入帧率为25
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # 获取视频高度
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # # 创建 VideoWriter对象
        self.now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        output = cv2.VideoWriter(self.now + '.avi', codec, fps, (frame_width, frame_height))
        if not (((len(sys.argv) == 2) and (self.cap.open(str(sys.argv[1]))))
                or (self.cap.open(self.CAM_NUM))):
            print("ERROR：No video file specified or camera connected.")
            return -1
        self.thread = Worker(self.MyUrl)
        self.thread.sinOut.connect(self.checkProcess)
        self.thread.start()

        while self.cap.isOpened():
            if self.switch:
                ret, frame = self.cap.read()
                cv2.putText(frame, self.subtitle + " " + self.now, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (55, 255, 155), 1)
                start_t = cv2.getTickCount()
                output.write(frame)
                stop_t = ((cv2.getTickCount() - start_t) / cv2.getTickFrequency()) * 1000
                key = cv2.waitKey(max(2, 40 - int(math.ceil(stop_t)))) & 0xFF
            else:
                print("Quit Process ")
                break


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
                self.live.setText(u'关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.video.clear()
            self.subtitle = ""
            self.live.setText(u'打开相机')

    def show_camera(self):
        # os.system(
        #    "/home/pi/mjpg-streamer/mjpg-streamer-experimental/start.sh")
        flag, self.image = self.cap.read()
        # face = self.face_detect.align(self.image)
        # if face:
        #     pass

        show = cv2.resize(self.image, (640, 480))
        s = time.asctime()
        cv2.putText(show, self.subtitle + " " + s, (10, 50), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 2)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.video.setPixmap(QtGui.QPixmap.fromImage(showImage))
        # self.x += 1
        # self.label_move.move(self.x,100)

        # if self.x ==320:
        #     self.label_show_camera.raise_()

    def setYellow(self):
        if self.yellowlight.isChecked():
            switch3_on = "sudo /home/pi/RPi_Relay_Board/shell/Relay.sh CH1 ON"
            os.system(switch3_on)
        else:
            switch3_off = "sudo /home/pi/RPi_Relay_Board/shell/Relay.sh CH1 OFF"
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
            switch1_on = "sudo /home/pi/RPi_Relay_Board/shell/Relay.sh CH2 ON"
            os.system(switch1_on)
        else:
            switch1_off = "sudo /home/pi/RPi_Relay_Board/shell/Relay.sh CH2 OFF"
            os.system(switch1_off)


class PrintWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Print Center')
        self.resize(600, 800)

        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    mainWindow = MainWindow()
    printWindow = PrintWindow()
    sys.exit(app.exec_())
