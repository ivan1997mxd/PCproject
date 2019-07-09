# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSlot, QUrl, QSizeF
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import QPrinter, QPrinterInfo
from PyQt5.QtGui import QTextDocument, QPainter, QImage
import sys, base64


class Printer:
    def __init__(self):
        self.p = QPrinterInfo.defaultPrinter()
        self.print_device = QPrinter(self.p)

    def print(self, content):
        self.print_device.setPageSizeMM(QSizeF(110, 250))
        d = QTextDocument()
        d.setDocumentMargin(0)
        d.setDefaultStyleSheet('''
        * {padding:0;margin: 0;}
        h1 {font-size: 20px;}
        h3 {font-size: 16px;}
        .left {float: left;}
        .right {float:right;}
        .clearfix {clear: both;}
        ul {list-style: none;}
        .print_container {width: 250px;}
        .section2 label {display: block;}
        .section3 label {display: block;}
        .section4 .total label {display: block;}
        .section4 {border-bottom: 1px solid #DADADA;}
        .section5 label {display: block;}
        ''')
        d.setHtml(content)
        d.print(self.print_device)

    def print_(self, data_url):
        image_content = base64.b64decode(data_url)  # 数据流base64解码
        image = QImage()
        image.loadFromData(image_content)  # 使用QImage构造图片
        painter = QPainter(self.print_device)  # 使用打印机作为绘制设备
        painter.drawImage(0, 0, image)  # 进行绘制（即调起打印服务）
        painter.end()  # 打印结束


class Print(QObject):
    def __init__(self):
        super().__init__()
        self.printer = Printer()

    @pyqtSlot(str, result=str)
    def print(self, content):
        self.printer.print(content)
        return

    @pyqtSlot(str, result=str)
    def print_(self, data_url):
        # 去除头部标识
        self.printer.print_(data_url.replace('data:image/png;base64,', ''))
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = QWebEngineView()
    browser.setWindowTitle('使用PyQt5打印热敏小票')
    browser.resize(900, 600)
    channel = QWebChannel()
    printer = Print()
    channel.registerObject('printer', printer)
    browser.page().setWebChannel(channel)
    url_string = "file:///python/print/webprint.html"  # 内置的网页地址
    browser.load(QUrl(url_string))
    browser.show()
    sys.exit(app.exec_())